# encoding: utf-8
# author: QCL
# datetime:2019/4/8 10:34
# software: PyCharm Professional Edition 2018.2.8


class Num(object):
    """获取当期开奖期号"""
    def __init__(self):
        self.ENGINE = input("请输入当期3D开奖期号：")


if __name__ == '__main__':
    a = Num()

