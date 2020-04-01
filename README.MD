# fc_3d

## 安装

### 安装Python3.5以上版本

## 安装Redis数据库

安装好之后开启redis数据库

### 配置fc_3d

```
cd fc_3d
```

进入fc_3d目录下，vim打开settings.py配置文件进行相关参数配置

1. REDIS_PASSWORD为redis登入密码，安装redis时如果没有配置密码则为 None
2. 如果使用本地网络被封ip, 则三方付费代理<阿布云代理隧道---动态版>用户名：proxyUser=xxx proxyPass=yyy

###安装三方依赖库

```
pip3 install -r requirements.txt
```

#### 打开fc_3d

```
python3 start.py
```
#### 如果打开fc_3d同时想打开API

进入fc_3目录下，vim打开settings.py文件修改API_ENABLED，默认为API_ENABLED = False不打开，打开则更改为True

### 代码运行如下：

```
请输入当期3D开奖期号：091
3D数据抓取开始运行...
请输入当期3D开奖期号：091
{'url': 'https://www.78500.cn/3dyuce/list-2.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/list-3.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/list-4.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/list-5.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/list-6.html', 'info': '抓取成功...', 'status_code': 200}
抓取当前页 https://www.78500.cn/3dyuce/5151798.html
{'url': 'https://www.78500.cn/3dyuce/5151798.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://expert.78500.cn/cj/3d/60127/?qishu=100', 'info': '抓取成功...', 'status_code': 200}
抓取当前页 https://www.78500.cn/3dyuce/5151794.html
{'url': 'https://www.78500.cn/3dyuce/5151794.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://expert.78500.cn/cj/3d/44887/?qishu=100', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/5151794.html', 'info': '抓取成功...', 'status_code': 200}
['×', '√', '√', '√', '√', '√']
抓取当前页 https://www.78500.cn/3dyuce/5151784.html
{'url': 'https://www.78500.cn/3dyuce/5151784.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://expert.78500.cn/cj/3d/45178/?qishu=100', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/5151784.html', 'info': '抓取成功...', 'status_code': 200}
['√', '√', '√', '√', '√', '√']
抓取当前页 https://www.78500.cn/3dyuce/5151771.html
{'url': 'https://www.78500.cn/3dyuce/5151771.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://expert.78500.cn/cj/3d/48418/?qishu=100', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/5151771.html', 'info': '抓取成功...', 'status_code': 200}
['√', '√', '×', '√', '√', '×']
...
抓取当前页 https://www.78500.cn/3dyuce/5149422.html
{'url': 'https://www.78500.cn/3dyuce/5149422.html', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://expert.78500.cn/cj/3d/46688/?qishu=100', 'info': '抓取成功...', 'status_code': 200}
{'url': 'https://www.78500.cn/3dyuce/5149422.html', 'info': '抓取成功...', 'status_code': 200}
['×', '√', '√', '√', '√', '√']
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
杀码统计汇总输出： {'9': '杀1刀', '2': '杀1刀', '6': '杀2刀', '8': '杀1刀'}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
数据抓取完毕...

```