# encoding: utf-8
# author: QCL
# datetime:2019/4/8 8:49
# software: PyCharm Professional Edition 2018.2.8
import time
from fc_3d_v3.settings import *
from fc_3d_v3.getter import Getter
from fc_3d_v3.api import app
from multiprocessing import Process


class Scheduler(object):

    @staticmethod
    def scheduler_getter(cycle=CYCLE):
        """
        定时抓取模块
        :param cycle: 抓取周期
        :return:
        """
        while True:
            getter = Getter()
            getter.run()
            time.sleep(cycle)

    @staticmethod
    def scheduler_api():
        """
        开启 web api 接口
        :return:
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        """启动调度器"""
        print("3D数据抓取开始运行...")

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()
