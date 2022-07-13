# -*- coding: utf-8 -*-

import uvicorn
from spider import Spider
from fastapi import FastAPI
from threading import Timer
from threading import Thread

data_zhihu = []  # 知乎
data_toutiao = []  # 头条
data_tieba = []  # 贴吧
data_baidu = []  # 百度
data_vsite = []  # V2EX
data_bsite = []  # B站
data_weibo = []  # 微博
data_shijiulou = []  # 19楼
data_cqmmgo = []  # cqmmgo
data_tianya = []  # 天涯
data_douyin = []  # 抖音
data_kuaishou = []  # 快手
data_a36kr = []  # 36kr
data_huxiu = []  # huxiu


s = Spider()


def run_tieba():
    global data_tieba
    data_tieba = s.spider_tieba()


def run_baidu():
    global data_baidu
    data_baidu = s.spider_baidu()


def run_zhihu():
    global data_zhihu
    data_zhihu = s.spider_zhihu()


def run_toutiao():
    global data_toutiao
    data_toutiao = s.spider_toutiao()


# def run_vsite():
#     global data_vsite
#     data_vsite = s.spider_vsite()


def run_weibo():
    global data_weibo
    data_weibo = s.spider_weibo()


def run_bsite():
    global data_bsite
    data_bsite = s.spider_bsite()


def run_shijiulou():
    global data_shijiulou
    data_shijiulou = s.spider_shijiulou()


def run_cqmmgo():
    global data_cqmmgo
    data_cqmmgo = s.spider_cqmmgo()


def run_tianya():
    global data_tianya
    data_tianya = s.spider_tianya()


def run_douyin():
    global data_douyin
    data_douyin = s.spider_douyin()


def run_kuaishou():
    global data_kuaishou
    data_kuaishou = s.spider_kuaishou()


def run_a36kr():
    global data_a36kr
    data_a36kr = s.spider_a36kr()


def run_huxiu():
    global data_huxiu
    data_huxiu = s.spider_huxiu()


# 此组15分钟采集一次
def task1():
    # 多线程运行
    Thread(target=run_zhihu, ).start()
    Thread(target=run_toutiao, ).start()
    Thread(target=run_tieba, ).start()
    Thread(target=run_baidu, ).start()
    Thread(target=run_weibo, ).start()
    # Thread(target=run_vsite, ).start()
    Thread(target=run_shijiulou, ).start()
    Thread(target=run_cqmmgo, ).start()
    Thread(target=run_tianya, ).start()
    Thread(target=run_douyin, ).start()
    Thread(target=run_kuaishou, ).start()
    Thread(target=run_a36kr, ).start()
    Thread(target=run_huxiu, ).start()
    Timer(15 * 60, task1, ).start()


# 此组每天采集一次，目前改为1小时
def task2():
    # 多线程运行
    Thread(target=run_bsite, ).start()
    Timer(1 * 60 * 60, task2, ).start()
    # Timer(24 * 60 * 60, task2, ).start()


task1()
task2()

app = FastAPI()


@app.get("/")
def index():
    return {'hello': 'world!o'}


@app.get("/hot/{name}")
def read_name(name: str):
    if name == 'zhihu':
        return data_zhihu
    elif name == 'toutiao':
        return data_toutiao
    elif name == 'vsite':
        return data_vsite
    elif name == 'weibo':
        return data_weibo
    elif name == 'tieba':
        return data_tieba
    elif name == 'baidu':
        return data_baidu
    elif name == 'bsite':
        return data_bsite
    elif name == '19lou':
        return data_shijiulou
    elif name == 'cqmmgo':
        return data_cqmmgo
    elif name == 'tianya':
        return data_tianya
    elif name == 'douyin':
        return data_douyin
    elif name == 'kuaishou':
        return data_kuaishou
    elif name == '36kr':
        return data_a36kr
    elif name == 'huxiu':
        return data_huxiu


if __name__ == '__main__':
    uvicorn.run(app=app,
                host="127.0.0.1",
                port=8080)
