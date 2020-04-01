# encoding: utf-8
# author: QCL
# datetime:2019/4/7 9:44
# software: PyCharm Professional Edition 2018.2.8


# 代理服务器及代理隧道验证信息设置
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"

# 下面两项代理用户和密码需要购买代理后手动设置
# 代理商地址：https://center.abuyun.com/login
PROXY_USER = "H4R245E4Z895V36D"
PROXY_PASS = "BB4225088B9A7C6E"


# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 使用哪个redis数据库，默认不设置时使用redis_db = 0
REDIS_DB = 1


# 默认请求头
DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/"
              "signed-exchange;v=b3;q=0.9",
    "accept-language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cookie": "UM_distinctid=1712f0928407fa-0fc1e15f3e0824-4313f6a-144000-1712f092841275; CNZZDATA3497249=cnzz_eid%3D"
              "420284903-1585631559-%26ntime%3D1585631559; CBBSESSID=4n2s4kop2j1du9p77k43o8hca5",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36",
}


# 数据连接入口
START_URL = "https://www.78500.cn/3dyuce/"

# 专家杀码历史数据连接
BASE_HISTORY_URL = "https://expert.78500.cn/cj/3d/{}/?qishu=100"

# 最差历史成绩阈值
LOW_THRESHOLD = 5

# 历史期数阈值
HISTORY_THRESHOLD = 96


# 生成模块配置字典
GETTER_MAP = {
    "caibaobei": "Getter"
}


# 抓取循环周期
CYCLE = 6*60*60

# web api 地址
API_HOST = "0.0.0.0"

# web api端口
API_PORT = 5000

# 抓取开关，默认为开启， 不想开启可更改为False
GETTER_ENABLED = True

# web api接口开关，默认为关闭，开启更改为True
API_ENABLED = False
