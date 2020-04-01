# encoding: utf-8
# author: QCL
# datetime:2019/4/7 9:44
# software: PyCharm Professional Edition 2018.2.8
import json
import redis
from fc_3d_v3.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        """
        初始化redis链接
        :param type: accounts or cookies
        :param website: 站点
        :param host: redis地址
        :param port: redis端口
        :param password: redis登入密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取hash名称
        :return: hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, author, value):
        """
        设置键值对
        :param author: 杀码作者
        :param value: 100_history or dalian_wrong or current_wrong
        :return: 添加的映射个数
        """
        return self.db.hset(self.name(), author, value)

    def get(self, author):
        """
        根据键名获取对应的键值
        :param author: 杀码作者
        :return: 杀码作者对应的 100_history or dalian_wrong or current_wrong
        """
        return self.db.hget(self.name(), author)

    def delete(self, author):
        """
        根据键名删除对应的键值
        :param author: 杀码作者
        :return: 作者100_history or dalian_wrong or current_wrong
        """
        return self.db.hdel(self.name(), author)

    def count(self):
        """
        获取数目
        :return:数目
        """
        return self.db.hlen(self.name())

    def author_names(self):
        """
        获取所有的作者杀码信息
        :return: (username,password) or (username, cookies)
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有的键值对
        :return: 所有键值对
        """
        return self.db.hgetall(self.name())

    def get_all_values(self):
        """
        获取所有的键值
        :return: 100_history or dalian_wrong or current_wrong
        """
        return self.db.hvals(self.name())


if __name__ == '__main__':
    # conn = RedisClient("100_history", "caibaobei")
    # res = conn.set("4425", {"1": 10, "3": 5, "4": 1, "2": 6})

    # conn = RedisClient("dalian_wrong", "caibaobei")
    # res = conn.set("4425", 3)

    # conn = RedisClient("current_wrong", "caibaobei")
    # res = conn.set("4425", 2)

    conn = RedisClient("current_wrong", "caibaobei")
    res = conn.all()

    print(json.dumps(res))

