# encoding: utf-8
# author: QCL
# datetime:2019/4/7 17:26
# software: PyCharm Professional Edition 2018.2.8
import json
from flask import Flask, g
from fc_3d_v3.settings import GETTER_MAP
from fc_3d_v3.db import RedisClient


__all__ = ['app']

app = Flask(__name__)


@app.route("/")
def index():
    """
    定义一个首页
    :return:
    """
    return '<h2>Welcome To 3D Pool System</h2>'


def get_conn():
    for website in GETTER_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_100_history', eval('RedisClient' + '("100_history", "' + website + '")'))
            setattr(g, website + '_current_equal_dalian_wrong', eval('RedisClient' + '("current_equal_dalian_wrong", \
            "' + website + '")'))
            setattr(g, website + '_current_gt_dalian_wrong', eval('RedisClient' + '("current_gt_dalian_wrong", \
            "' + website + '")'))
            setattr(g, website + '_dalian_wrong', eval('RedisClient' + '("dalian_wrong", "' + website + '")'))
            setattr(g, website + '_summary_wrong', eval('RedisClient' + '("summary_wrong", "' + website + '")'))

    return g


@app.route("/<website>/history")
def get_100_history(website):
    """
    获取所有作者杀一码100期历史数据
    :param website: 抓取网站
    :return: 所有作者100期历史数据
    """
    g = get_conn()
    all_author_history_info = getattr(g, website + '_100_history').all()

    return json.dumps(all_author_history_info)


@app.route("/<website>/current_equal_dalian_wrong")
def get_current_equal_dalian_wrong(website):
    """
    获取所有当前连错等于最大历史连错
    :param website: 抓取网站
    :return: 当前连错信息
    """
    g = get_conn()
    all_current_equal_dalian_wrong_info = getattr(g, website + '_current_equal_dalian_wrong').all()

    return json.dumps(all_current_equal_dalian_wrong_info)


@app.route("/<website>/current_gt_dalian_wrong")
def get_current_gt_dalian_wrong(website):
    """
    当前连错大于历史最大连错
    :param website: 抓取网站
    :return: 当前连错信息
    """
    g = get_conn()
    all_current_gt_dalian_wrong_info = getattr(g, website + '_current_gt_dalian_wrong').all()

    return json.dumps(all_current_gt_dalian_wrong_info)


@app.route("/<website>/dalian_wrong")
def get_dalian_wrong(website):
    """
    获取所有作者杀码历史最大连错信息
    :param website: 抓取站点
    :return: 杀码最大连错信息
    """
    g = get_conn()
    all_dalian_wrong_info = getattr(g, website + '_dalian_wrong').all()

    return json.dumps(all_dalian_wrong_info)


@app.route("/<website>/summary_wrong")
def get_summary_wrong(website):
    """
    杀码统计汇总输出
    :param website:抓取站点
    :return: 杀码统计输出
    """
    g = get_conn()
    summary_wrong_data = getattr(g, website + "_summary_wrong").all()

    return json.dumps(summary_wrong_data)


if __name__ == '__main__':
    app.run()
