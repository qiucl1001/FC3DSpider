# encoding: utf-8
# author: QCL
# datetime:2019/4/8 8:00
# software: PyCharm Professional Edition 2018.2.8

import requests


# 默认请求头
BASE_HEADERS = {
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


def get_page(url, options={}):
    """抓取网页"""
    headers = dict(BASE_HEADERS, **options)

    try:
        response = requests.get(url=url, headers=headers)
        url = response.url
        status_code = response.status_code
        if response.status_code == 200:
            print({"info": "抓取成功...", "url": url, "status_code": status_code})
            return response
        else:
            print({"info": "抓取失败...", "url": url, "status_code": status_code})
    except Exception as e:
        print("抓取失败...")
        raise e

