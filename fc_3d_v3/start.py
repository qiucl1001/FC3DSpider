# encoding: utf-8
# author: QCL
# datetime:2019/4/8 9:10
# software: PyCharm Professional Edition 2018.2.8
from fc_3d_v3.scheduler import Scheduler


def main():

    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print(e.args)
        main()


if __name__ == '__main__':
    main()
