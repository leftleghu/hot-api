# -*- coding: utf-8 -*-

import json
import re
import requests
import datetime
from lxml import etree
from threading import Timer

# vsite_api = "https://www.v2ex.com/?tab=hot"
# bsite_api = 'https://www.bilibili.com/v/popular/rank/all'

bsite_api = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
weibo_api = "https://s.weibo.com/top/summary?cate=realtimehot"
tieba_api = "http://tieba.baidu.com/hottopic/browse/topicList?res_type=1"
zhihu_api = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
baidu_api = 'https://top.baidu.com/board?tab=realtime'
shijiulou_api = 'https://www.19lou.com/r/1/rd.html'
cqmmgo_api = 'https://go.cqmmgo.com/r/82/syttsl.html'
jiaxing_api = 'https://jiaxing.19lou.com/r/58/jrrd.html'
taizhou_api = 'https://taizhou.19lou.com/r/37/rd.html'
toutiao_api = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
douban_api = 'https://www.douban.com/gallery/'
douyin_api = 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/'
kuaishou_api = 'https://www.kuaishou.com/brilliant'
huxiu_api = 'https://www.huxiu.com/'
hupu_api = 'https://bbs.hupu.com/topic-daily-hot'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
headers_weibo = {
    'host': 's.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'cookie': 'xxxxxxxx'
}
headers_bsite = {
    # 'host': 'www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
headers_shijiulou = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'cookie': 'xxxxxxxx'
}


# 组装数据1
def packdata(para_data):
    list_data = []
    for i in para_data:
        data = {}
        data["title"] = i[0]
        data["url"] = i[1]
        data["zhishu"] = i[2]
        list_data.append(data)
    return list_data


class Spider(object):
    def __init__(self, url=None):
        if url is not None:
            self.url = url
            if url == weibo_api:
                self.res = requests.get(url, headers=headers_weibo)
            elif url == bsite_api:
                self.res = requests.get(url, headers=headers_bsite)
            elif url == shijiulou_api:
                self.res = requests.get(url, headers=headers_shijiulou)
                self.res.encoding = "gbk"
            elif url == cqmmgo_api:
                self.res = requests.get(url, headers=headers_shijiulou)
                self.res.encoding = "gbk"
            elif url == jiaxing_api:
                self.res = requests.get(url, headers=headers_shijiulou)
                self.res.encoding = "gbk"
            elif url == taizhou_api:
                self.res = requests.get(url, headers=headers_shijiulou)
                self.res.encoding = "gbk"
            else:
                self.res = requests.get(url, headers=headers)
                self.res.encoding = "utf-8"
            self.soup = etree.HTML(self.res.text)

    # 知乎热榜
    def spider_zhihu(self):
        ex = 'https://www.zhihu.com/question/'
        list_zhihu = []  # 此列表用于储存解析结果
        res = Spider(zhihu_api).res
        # 逐步解析接口返回的json
        zhihu_data = json.loads(res.text)['data']
        for part_zhihu_data in zhihu_data:  # 遍历每一个data对象
            zhihu_id = part_zhihu_data['target']['id']  # 从对象得到问题的id
            zhihu_url = ex + str(zhihu_id)
            zhihu_title = part_zhihu_data['target']['title']  # 从对象得到问题的title
            zhihu_answer = part_zhihu_data['target']['answer_count']
            zhihu_follower = part_zhihu_data['target']['follower_count']
            zhihu_zhishu = str(zhihu_follower) + "/" + str(zhihu_answer)
            list_zhihu.append([zhihu_title, zhihu_url, zhihu_zhishu])  # 将id 和title组为一个列表，并添加在list_zhihu列表中
        return packdata(list_zhihu)

    # 头条热榜
    def spider_toutiao(self):

        list_toutiao = []  # 此列表用于储存解析结果
        res = Spider(toutiao_api).res
        # 逐步解析接口返回的json
        toutiao_data = json.loads(res.text)['data']
        for part_toutiao_data in toutiao_data:  # 遍历每一个data对象
            toutiao_url = part_toutiao_data['Url']  # 从对象得到问题的id
            toutiao_title = part_toutiao_data['Title']  # 从对象得到问题的title
            toutiao_zhishu_ori = part_toutiao_data['HotValue']
            toutiao_zhishu = str(round(int(toutiao_zhishu_ori)/10000, 1)) + "万"

            list_toutiao.append([toutiao_title, toutiao_url, toutiao_zhishu])  # 将id 和title组为一个列表，并添加在list_zhihu列表中
        return packdata(list_toutiao)

    # 微博热搜
    def spider_weibo(self):
        list_weibo = []  # 此列表用于储存解析结果
        weibo = "https://s.weibo.com"
        soup = Spider(weibo_api).soup
        # for soup_a in soup.xpath("//td[@class='td-02']/a"):
        #     wb_title = soup_a.text
        #     wb_url = weibo + soup_a.get('href')
        for soup_a in soup.xpath("//td[@class='td-02']")[1:]:
            wb_title = soup_a.xpath(".//a/text()")[0]
            wb_url = weibo + soup_a.xpath(".//a/@href")[0]
            wb_zhishu_ori = soup_a.xpath('normalize-space(.//span/text())')
            if wb_zhishu_ori.isdigit():
                wb_zhishu = str(round(int(wb_zhishu_ori)/10000, 1)) + "万"
            else:
                wb_zhishu = wb_zhishu_ori
            # 过滤微博的广告，做个判断
            if "javascript:void(0)" in wb_url:
                pass
            else:
                list_weibo.append([wb_title, wb_url, wb_zhishu])
        return packdata(list_weibo)

    # 贴吧热度榜单
    def spider_tieba(self):
        list_tieba = []
        soup = Spider(tieba_api).soup
        # for soup_a in soup.xpath("//a[@class='topic-text']"):
        #     tieba_title = soup_a.text
        #     tieba_url = soup_a.get('href')
        for soup_a in soup.xpath("//div[@class='topic-name']"):
            tieba_title = soup_a.xpath(".//a[@class='topic-text']/text()")[0]
            tieba_url = soup_a.xpath(".//a[@class='topic-text']/@href")[0]
            tieba_zhishu_ori = soup_a.xpath(".//span[@class='topic-num']/text()")[0]
            tieba_zhishu = tieba_zhishu_ori.replace('实时讨论', '')
            list_tieba.append([tieba_title, tieba_url, tieba_zhishu])
        return packdata(list_tieba)

    # 百度热度榜单
    def spider_baidu(self):
        list_baidu = []
        soup = Spider(baidu_api).soup
        # for soup_url in soup.xpath("//*[@class='content_1YWBm']/a"):
        #     baidu_url = soup_url.get('href')
        # for soup_title in soup.xpath("//*[@class='c-single-text-ellipsis']/text()"):
        #     baidu_title = soup_title
        for i in range(1, 31):
            baidu_title = soup.xpath(
                "//*[@id='sanRoot']/main/div[2]/div/div[2]/div[" + str(i) + "]/div[2]/a/div[1]/text()")[0]
            baidu_url = soup.xpath("//*[@id='sanRoot']/main/div[2]/div/div[2]/div[" + str(i) + "]/div[2]/a/@href")[0]
            baidu_zhishu_ori = soup.xpath(
                "//*[@id='sanRoot']/main/div[2]/div/div[2]/div[" + str(i) + "]/div[1]/div[2]/text()")[0]
            baidu_zhishu = str(round(int(baidu_zhishu_ori)/10000, 1)) + "万"
            # print(baidu_title, baidu_url, baidu_zhishu)
            list_baidu.append([baidu_title, baidu_url, baidu_zhishu])
        return packdata(list_baidu)

    # V2EX热度榜单
    # def spider_vsite(self):
    #     list_v2ex = []
    #     vsite = "https://www.v2ex.com"
    #     soup = Spider(vsite_api).soup
        # for soup_a in soup.xpath("//span[@class='item_title']/a"):
        #     vsite_title = soup_a.text
        #     vsite_url = vsite + soup_a.get('href')
        #     vsite_zhishu = soup_a.xpath("//a[@class='count_livid']/text()")
        # vsite_title = vsite_b.text
        # vsite_url = vsite + vsite_b.get('href')

        # for soup_a in soup.xpath("//div[@class='cell item']"):
        #     vsite_title = soup_a.xpath(".//span[@class='item_title']/a/text()")[0]
        #     vsite_url = vsite + soup_a.xpath(".//span[@class='item_title']/a/@href")[0]
        #     vsite_zhishu = soup_a.xpath(".//a[@class='count_livid']/text()")[0]
        #     # print(vsite_zhishu)
        #     list_v2ex.append([vsite_title, vsite_url, vsite_zhishu])
        # return packdata(list_v2ex)

    # B站排行榜
    def spider_bsite(self):
        list_bsite = []
        # ex = 'https:'
        # soup = Spider(bsite_api).soup
        res = Spider(bsite_api).res
        bsite_data = json.loads(res.text)['data']['list']
        # print(res.text)
        for i in bsite_data:
            bsite_title = i['title']
            bsite_url = i['short_link_v2']
            bsite_play_ori = i['stat']['view']
            bsite_play = str(round(bsite_play_ori/10000, 1)) + "万"
            bsite_like_ori = i['stat']['like']
            bsite_like = str(round(bsite_like_ori/10000, 1)) + "万"
            bsite_zhishu = str(bsite_play) + "/" + str(bsite_like)
            list_bsite.append([bsite_title, bsite_url, bsite_zhishu])
        return packdata(list_bsite)

    # 19lou排行榜
    def spider_shijiulou(self):
        list_shijiulou = []
        ex = 'https:'
        soup = Spider(shijiulou_api).soup
        for i in soup.xpath("//div[starts-with(@id,'J_item_')]"):
            shijiulou_title = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@title)')
            shijiulou_url = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@href)')
            shijiulou_read = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[1]/em/text())')
            shijiulou_reply = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[2]/em/text())')
            shijiulou_zhishu = shijiulou_read + "/" + shijiulou_reply
            # print(shijiulou_zhishu)
            list_shijiulou.append([shijiulou_title, shijiulou_url, shijiulou_zhishu])
        return packdata(list_shijiulou)

    # 重庆购物狂排行榜
    def spider_cqmmgo(self):
        list_cqmmgo = []
        ex = 'https:'
        soup = Spider(cqmmgo_api).soup
        for i in soup.xpath("//div[starts-with(@id,'J_item_')]"):
            cqmmgo_title = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@title)')
            cqmmgo_url = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@href)')
            cqmmgo_read = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[1]/em/text())')
            cqmmgo_reply = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[2]/em/text())')
            cqmmgo_zhishu = cqmmgo_read + "/" + cqmmgo_reply
            # print(shijiulou_zhishu)
            list_cqmmgo.append([cqmmgo_title, cqmmgo_url, cqmmgo_zhishu])
        return packdata(list_cqmmgo)

    # 嘉兴19楼排行榜
    def spider_jiaxing(self):
        list_jiaxing = []
        ex = 'https:'
        soup = Spider(jiaxing_api).soup
        for i in soup.xpath("//div[starts-with(@id,'J_item_')]"):
            jiaxing_title = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@title)')
            jiaxing_url = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@href)')
            jiaxing_read = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[1]/em/text())')
            jiaxing_reply = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[2]/em/text())')
            jiaxing_zhishu = jiaxing_read + "/" + jiaxing_reply
            # print(shijiulou_zhishu)
            list_jiaxing.append([jiaxing_title, jiaxing_url, jiaxing_zhishu])
        return packdata(list_jiaxing)

    # 台州19楼排行榜
    def spider_taizhou(self):
        list_taizhou = []
        ex = 'https:'
        soup = Spider(taizhou_api).soup
        for i in soup.xpath("//div[starts-with(@id,'J_item_')]"):
            taizhou_title = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@title)')
            taizhou_url = i.xpath('normalize-space(.//div[@class="item-bd"]/div/a/@href)')
            taizhou_read = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[1]/em/text())')
            taizhou_reply = i.xpath('normalize-space(.//div[@class="item-ft"]/p/span[2]/em/text())')
            taizhou_zhishu = taizhou_read + "/" + taizhou_reply
            # print(taizhou_zhishu)
            list_taizhou.append([taizhou_title, taizhou_url, taizhou_zhishu])
        return packdata(list_taizhou)

    # 豆瓣热搜
    def spider_douban(self):
        list_douban = []
        soup = Spider(douban_api).soup
        for soup_a in soup.xpath("//ul[@class='trend']/li"):
            douban_title = soup_a.xpath(".//a/text()")[0]
            # print(douban_title)
            douban_url = soup_a.xpath(".//a/@href")[0]
            # print(douban_url)
            douban_zhishu_ori = soup_a.xpath(".//span/text()")[0]
            chinese_chars = ''.join([chr(i) for i in range(0x4e00, 0x9fff)])
            douban_zhishu_ori_num = douban_zhishu_ori.translate(str.maketrans('', '', chinese_chars))
            douban_zhishu = str(douban_zhishu_ori_num) + "万"
            # print(douban_zhishu_ori_num)
            list_douban.append([douban_title, douban_url, douban_zhishu])
        return packdata(list_douban)

        # list_tianya = []  # 此列表用于储存解析结果
        # res = Spider(tianya_api).res
        # # 逐步解析接口返回的json
        # tianya_data = json.loads(res.text)['data']['rows']
        # # print(tianya_data)
        # for part_tianya_data in tianya_data:  # 遍历每一个data对象
        #     tianya_title = part_tianya_data['title']  # 从对象得到问题的title
        #     tianya_url = part_tianya_data['url']  # 从对象得到问题的url
        #     tianya_zhishu = part_tianya_data['count']  # 从对象得到问题的回复数
        #     list_tianya.append([tianya_title, tianya_url, tianya_zhishu])  # 将title和url组为一个列表，并添加在list_tianya列表中
        # return packdata(list_tianya)

    # 抖音热榜
    def spider_douyin(self):
        list_douyin = []  # 此列表用于储存解析结果
        ex = 'https://www.douyin.com/search/'
        res = Spider(douyin_api).res
        # 逐步解析接口返回的json
        douyin_data = json.loads(res.text)['word_list']
        for part_douyin_data in douyin_data:  # 遍历每一个data对象
            # print(part_douyin_data)
            douyin_title = part_douyin_data['word']  # 从对象得到问题的title
            douyin_url = ex + part_douyin_data['word']  # 从对象得到问题的url
            douyin_zhishu_ori = part_douyin_data['hot_value']  # 从对象得到问题的回复数
            douyin_zhishu = str(round(douyin_zhishu_ori/10000, 1)) + "万"
            list_douyin.append([douyin_title, douyin_url, douyin_zhishu])  # 将title和url组为一个列表，并添加在list_tianya列表中
        return packdata(list_douyin)

    def spider_kuaishou(self):
        list_kuaishou = []  # 此列表用于储存解析结果
        ex = 'https://www.kuaishou.com/search/video?searchKey='
        soup = Spider(kuaishou_api).soup
        soup_a = soup.xpath('//script/text()')[1]
        # print(soup_a)
        soup_b = re.search(r"window\.__APOLLO_STATE__=(.*?);", soup_a).group(1)
        kuaishou_data = json.loads(soup_b, strict=False)
        kuaishou_ids = kuaishou_data['defaultClient']['$ROOT_QUERY.visionHotRank({\"page\":\"brilliant\"})']['items']
        # print(kuaishou_ids)
        for kuaishou_id in kuaishou_ids:
            kuaishou_key = kuaishou_id['id']
            kuaishou_title = kuaishou_data['defaultClient'][kuaishou_key]['name']
            kuaishou_url = ex + kuaishou_title
            kuaishou_zhishu = kuaishou_data['defaultClient'][kuaishou_key]['hotValue']
            list_kuaishou.append([kuaishou_title, kuaishou_url, kuaishou_zhishu])
        return packdata(list_kuaishou)

    def spider_a36kr(self):
        today = datetime.date.today()
        a36kr_api = 'https://36kr.com/hot-list/zonghe/{}/1'.format(today)
        list_a36kr = []  # 此列表用于储存解析结果
        ex = 'https://36kr.com/p/'
        soup = Spider(a36kr_api).soup
        soup_a = soup.xpath('//body/script/text()')[0]
        soup_aa = soup_a + "leftleg"
        soup_b = re.search(r"window\.initialState=(.*?)leftleg", soup_aa).group(1)
        a36kr_data = json.loads(soup_b, strict=False)
        a36kr_ids = a36kr_data['hotListDetail']['articleList']['itemList']

        for a36kr_id in a36kr_ids:
            a36kr_key = a36kr_id['itemId']
            a36kr_title = a36kr_id['widgetTitle']
            a36kr_zhishu = a36kr_id['statCollect']
            # print(a36kr_zhishu)
            a36kr_url = ex + str(a36kr_key)

            list_a36kr.append([a36kr_title, a36kr_url, a36kr_zhishu])
        return packdata(list_a36kr)

    def spider_huxiu(self):
        list_huxiu = []  # 此列表用于储存解析结果
        ex = 'https://36kr.com/p/'
        soup = Spider(huxiu_api).soup
        soup_a = soup.xpath('//script/text()')[0]
        print(soup_a)
        soup_b = re.search(r"window\.__INITIAL_STATE__=(.*?);", soup_a).group(0)
        # soup_c = soup_b.replace("u002F", '')
        # print(soup_c)
        huxiu_data = json.loads(soup_b, strict=False)
        huxiu_ids = huxiu_data['news']['hotArticles']
        # print(huxiu_ids)
        #
        for huxiu_id in huxiu_ids:
            huxiu_title = huxiu_id['title']
            huxiu_url = huxiu_id['url']
            huxiu_zhishu = huxiu_id['count_info']['favorite_num']
            # huxiu_url_ori = huxiu_id['share_url']
            # huxiu_url = huxiu_url_ori.replace("m.", "www.")
            # huxiu_zhishu_ori = huxiu_id['count_info']['favorite_num']
            # huxiu_zhishu = str(round(huxiu_zhishu_ori/10000, 1)) + "万"
            list_huxiu.append([huxiu_title, huxiu_url, huxiu_zhishu])
        return packdata(list_huxiu)

    # 虎扑步行街主干道热度榜单
    def spider_hupu(self):
        list_hupu = []
        ex = 'https://bbs.hupu.com'
        soup = Spider(hupu_api).soup
        for soup_a in soup.xpath("//div[@class='bbs-sl-web-post-layout']"):
            hupu_title = soup_a.xpath(".//a[@class='p-title']/text()")[0]
            # print(hupu_title)
            hupu_url_ori = soup_a.xpath(".//a[@class='p-title']/@href")[0]
            hupu_url = ex + hupu_url_ori
            hupu_zhishu = soup_a.xpath(".//div[@class='post-datum']/text()")[0]
            # print(hupu_zhishu)
            list_hupu.append([hupu_title, hupu_url, hupu_zhishu])
        return packdata(list_hupu)

# Spider().spider_bsite()
