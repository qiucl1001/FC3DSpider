# encoding: utf-8
# author: QCL
# datetime:2019/4/7 10:28
# software: PyCharm Professional Edition 2018.2.8
import re
import time
# import json
import requests
from lxml import etree
from collections import Counter
from fc_3d_v3.db import RedisClient
from fc_3d_v3.libs_proxy import SetProxy
from fc_3d_v3.utils import get_page
from fc_3d_v3.lottery import Num
from fc_3d_v3.settings import DEFAULT_HEADERS, START_URL, BASE_HISTORY_URL, LOW_THRESHOLD, HISTORY_THRESHOLD


class Getter(object):
    def __init__(self, start_url=START_URL, headers=DEFAULT_HEADERS, history_url=BASE_HISTORY_URL, engine=Num().ENGINE):
        self.start_url = start_url
        self.headers = headers
        self.engine = engine
        self.history_url = history_url

        self.expert_links = list()
        self.count = 0  # 计数请求帖子链接，判断项目运行完是否手动关闭，因为代码部署到服务器设置爬取周期为6小时

        self.kill_nums = list()

        self.history_db = RedisClient("100_history", "caibaobei")  # 历史数据
        self.dalian_wrong_db = RedisClient("dalian_wrong", "caibaobei")  # 最大连错
        self.current_equal_dalian_wrong_db = RedisClient("current_equal_dalian_wrong", "caibaobei")  # 当前连错等于最大连错
        self.current_gt_dalian_wrong_db = RedisClient("current_gt_dalian_wrong", "caibaobei")  # 当前连错大于历史最大连错
        self.summary_wrong_db = RedisClient("summary_wrong", "caibaobei")  # 当前连错统计汇总

        self.set_proxy = SetProxy()  # 创建一个获取代理对象

    def run(self):
        """
        运行爬虫
        :return:
        """
        try:
            # 使用本地网络访问
            response = requests.get(url=self.start_url, headers=self.headers)
        except Exception as e:
            print(e.args)
            # 使用代理
            response = self.set_proxy.get_page(self.start_url)
            self.get_current_page_links(response)

        self.get_current_page_links(response)

    def get_current_page_links(self, response):
        """
        获取当前页的所有专家发帖数据连接
        :param response: 当前入口网页经过解码后的响应数据Xpath对象，类型为str
        :return:
        """
        res = response.text
        html = etree.HTML(res)

        # 提取当前页所有发帖的链接
        profile_links = html.xpath('//div[@class="main"]//div[@class="list-content"]/ul/li//a/@href')

        # 提取当前页所有发帖的标题
        primary_titles = html.xpath('//div[@class="main"]//div[@class="list-content"]/ul/li//a/text()')

        # 对标题预处理，剔除冒号(：)后面的标题数据
        profile_titles = list(map(lambda x: x.split("：")[0], primary_titles))

        # 筛选出每个发帖标题中的开奖期号，并转化为字符串预存储在title_list列表容器中
        title_list = list()
        for title in profile_titles:
            num = "".join(re.findall(r"{}".format(self.engine), title))
            title_list.append(num)

        # 把发帖链接url与标题中提取出来的期号拼接成新的字符串保存在zip_links列表容器中
        zip_links = list(zip(profile_links, title_list))
        zip_links = list(map(lambda x: "".join(x), zip_links))

        # 筛选出当前页所有双色球当期开奖的发帖链接url并且保存在初始化好的空列表expert_links中，目的是通过列表长度控制翻页
        offset = 0
        for i in zip_links:
            if i.endswith("{}".format(self.engine)):
                i = i.replace("{}".format(self.engine), "")
                self.expert_links.append(i)
                offset += 1

        print(self.expert_links)
        print("==" * 100)
        print("累计到当前页当期总链接数：%d, 当前页当期链接数：%d" % (len(self.expert_links), offset))

        # 控制翻页
        next_url = html.xpath('//a[text()="下一页"]/@href')[0]
        if 0 == len(self.expert_links) % 35 and offset != 0:
            time.sleep(2)
            self.get_next_page_links(next_url)
        else:
            self.get_author_id()

    def get_next_page_links(self, next_url):
        try:
            # 使用本地网络访问
            response = requests.get(url=next_url, headers=self.headers)
        except Exception as e:
            print(e.args)
            # 使用代理
            response = self.set_proxy.get_page(next_url)
        if response:
            self.get_current_page_links(response)

    def get_author_id(self):
        """提取作者专栏链接id并通过id构造对应的历史数据链接"""
        for expert_link in self.expert_links:
            print("抓取当前页", expert_link)
            self.count += 1
            try:
                # 使用本地网络
                response = get_page(expert_link)
            except Exception as e:
                print(e.args)
                # 使用代理
                response = self.set_proxy.get_page(expert_link)
            if response:
                text = response.text
                html = etree.HTML(text)

                # 作者专栏连接
                try:
                    column_link = html.xpath("//div[@class='main']//div[@class='main-hd-content']/p[last()]/a[1]/@href")[0]
                    author_id = column_link.split("/")[-2]
                    # 构造杀码专家历史数据url
                    history_link = self.history_url.format(author_id)
                    self.parse_detail_page(history_link, author_id)
                except IndexError:
                    print("reason: list index out of range")
                # break
            time.sleep(0.5)

    def parse_detail_page(self, history_link, author_id):
        """
        提取作者100最近100期杀码历史数据
        :param history_link: 历史数据连接
        :param author_id: 历史数据连接地址标识
        :return:
        """
        try:
            # 使用本地网络
            response = get_page(history_link)
        except Exception as e:
            print(e.args)
            # 使用代理
            response = self.set_proxy.get_page(history_link)
        if response:
            text = response.text
            html = etree.HTML(text)
            # 杀一码100期历史对错战绩
            history_100_data = html.xpath("//table[@class='cjtable']/tbody[@id='info']/tr[position()<101]"
                                          "/td[8]/font[1]/text()")

            # 杀一码100期历史前96期对错战绩
            history_96_data = history_100_data[:-4]

            # 杀一码100期历史最近6期对错战绩
            current_6_data = history_100_data[-6:]

            # 当前期预测数据连接url
            predict_url = html.xpath("//table[@class='cjtable']/tbody[@id='info']/tr[last()]/td[last()]/a/@href")[0]

            if len(history_96_data) == HISTORY_THRESHOLD:
                """
                统计各个作者3D杀一码100期历史中杀错情况e.g:如下
                # 1. al头"x"尾"√"
                al = ["x", "x", "√", "√", "x", "x", "x", "√",  "x", "√",  "x", "√", "x", "x", "x", "x", "√"]
                # 2. al头"x"尾"×"
                al = ["x", "x", "√", "√", "x", "x", "x", "√",  "x", "√",  "x", "√", "x", "x", "x", "x"]
                # 3. al头"√"尾"×"
                al = ["√", "x", "x", "√", "√", "x", "x", "x", "√",  "x", "√",  "x", "√", "x", "x", "x", "x"]
                # 4. al头"√"尾"√"
                al = ["√", "x", "x", "√", "√", "x", "x", "x", "√",  "x", "√",  "x", "√", "x", "x", "x", "x", "√"]
                输出结果：count_list = [2,3,1,1,4]    
                """
                count_list = list()
                flag_x = 0
                flag_y = 0
                for index, value in enumerate(history_96_data):
                    if value == "×":
                        flag_x += 1
                        if index == len(history_96_data) - 1 and history_96_data[len(history_96_data) - 1] == "×":
                            count_list.append(flag_x)
                        flag_y = 0
                    else:
                        if flag_y == 0:
                            if index == 0:
                                continue
                            else:
                                count_list.append(flag_x)
                            flag_x = 0
                            flag_y += 1
                        flag_y += 1

                max_wrong = max(Counter(count_list))

                # 筛选出满100期历史且最大连错允许为4的所有作者杀码数据
                if (history_96_data[0] == '×' and max_wrong < LOW_THRESHOLD) or \
                        (history_96_data[0] == '√' and max_wrong < LOW_THRESHOLD):
                    history_detail = dict(Counter(count_list))
                    self.dalian_wrong_db.set(author_id, max_wrong)
                    self.history_db.set(author_id, history_detail)

                self.current_wrong_info(author_id, current_6_data, predict_url, max_wrong)

    def current_wrong_info(self, author_id, current_6_data, predict_url, max_wrong):
        """
        提取最近4期连错情况(2连错/3连错/4连错)
        :param author_id: 作者100期历史连接地址标识
        :param current_6_data: 100期历史最近6期杀码数据
        :param predict_url: 100期历史数据网页中提取出当前开奖期的预测数据连接
        :param max_wrong: 100期历史前96期最大连错
        :return:
        """
        try:
            # 使用本地网络
            response = get_page(predict_url)
        except Exception as e:
            print(e.args)
            # 使用代理
            response = self.set_proxy.get_page(predict_url)
        if response:
            text = response.text
            html = etree.HTML(text)
            kill_num = html.xpath("//table[@class='main-hd-tab']//tr[4]/td[@class='s-left']/text()")[0]
            # print(kill_num)
            # print("~"*20)

            latest_kill_history = current_6_data[::-1]
            print(latest_kill_history)

            # 最近一期
            latest = latest_kill_history[0]
            # 倒数第二期
            second = latest_kill_history[1]
            # 倒数第三期
            third = latest_kill_history[2]
            # 倒数第四期
            fourth = latest_kill_history[3]
            # 倒数第五期
            fifth = latest_kill_history[4]
            # 倒数第六期
            six = latest_kill_history[5]

            # 通过字典映射这种数据结构优化上面多个if判断条件
            fc_3d_dic = {
                "4>3": latest == second == third == fourth == '×' and fifth == '√' and max_wrong == 3,
                "4>2": latest == second == third == fourth == '×' and fifth == '√' and max_wrong == 2,
                "4>1": latest == second == third == fourth == '×' and fifth == '√' and max_wrong == 1,
                "3>2": latest == second == third == '×' and fourth == '√' and max_wrong == 2,
                "3>1": latest == second == third == '×' and fourth == '√' and max_wrong == 1,
                "2>1": (latest == second == '×' and third == fourth == '√' and max_wrong == 1) or \
                       (latest == second == fourth == '×' and third == fifth == '√' and max_wrong == 1),
                "4": latest == second == third == fourth == '×' and fifth == '√' and max_wrong == 4,
                "3": latest == second == third == '×' and fourth == '√' and max_wrong == 3,
                "2": (latest == second == '×' and third == fourth == '√' and max_wrong == 2) or \
                    (latest == second == fourth == '×' and third == fifth == '√' and max_wrong == 2) or \
                    (latest == second == fourth == fifth == '×' and third == six == '√' and max_wrong == 2)
            }
            for key, value in fc_3d_dic.items():
                if value:
                    self.kill_nums.append(kill_num)
                    self.current_gt_dalian_wrong_db.set(author_id, {key: kill_num})
                    # redis3.0+ 将字典序列化后在存储
                    # self.current_gt_dalian_wrong_db.set(author_id, json.dumps({key: kill_num}))

        if self.count == len(self.expert_links):
            dic = dict(Counter(self.kill_nums))
            qcl = {}
            for i in dic.items():
                qcl["{}".format(i[0])] = "杀{}刀".format(i[1])
            self.summary_wrong_db.set("杀码统计汇总输出", qcl)

            print("~"*100)
            print("杀码统计汇总输出：", qcl)
            print("~"*100)
            print("数据抓取完毕...")


if __name__ == '__main__':
    spider = Getter()
    spider.run()


