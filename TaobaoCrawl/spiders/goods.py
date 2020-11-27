import copy
import re
import time
from threading import Lock

import scrapy
from scrapy import Request

from TaobaoCrawl.items import TaobaocrawlItem
from TaobaoCrawl.utils.cookie_utils import Cookie_Utils
from TaobaoCrawl.utils.db_controller_mysql import MySql_Utils


class GoodsSpider(scrapy.Spider):
    name = 'goods'

    def __init__(self):

        # 爬取总数
        self.totalCount = 0
        self.mutex = Lock()  # 线程锁保证线程安全


        #动态cookie
        self.cookie_utils = Cookie_Utils()
        #伪造请求头
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.mysql_utils = MySql_Utils()

        #搜索词
        self.search_word_list=["眼镜","面霜"]

    def start_requests(self):
        '''准备开始爬取首页数据
        :return:
        '''
        for index in range(len(self.search_word_list)):
            q = self.search_word_list[index]
            data_value = 0 #第几页，每页44条信息
            t = time.time()
            _ksTS = int(round(t * 1000))
            staobaoz = time.strftime('%Y%m%d', time.localtime(t))
            #根据销量排行爬取
            req_url = f"https://s.taobao.com/search?data-key=sort&data-value=sale-desc&ajax=true&_ksTS={_ksTS}_794&q={q}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{staobaoz}&ie=utf8"
            meta = {"q": q, "data_value": data_value}
            req_headers = copy.deepcopy(self.headers)
            req_headers["Referer"] = req_url
            req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
            print(f"准备爬取[{q}]第[1]页req_url=[{req_url}]的列表信息\n")
            yield Request(url=req_url, method='GET', headers=req_headers, callback=self.pagination_parse, meta=meta,
                          dont_filter=True)

    def pagination_parse(self, response):
        text_json = response.json()

        q = response.meta.get('q')
        data_value = response.meta.get('data_value')

        url = text_json.get("url", "")
        if ("https://s.taobao.com:443//search/" in url):
            print("cookie失效了，请更换cookie")
        else:
            currentPage = text_json.get("mods").get("pager").get("data").get("currentPage")
            pageSize = text_json.get("mods").get("pager").get("data").get("pageSize")
            totalPage = text_json.get("mods").get("pager").get("data").get("totalPage")
            # totalCount = text_json.get("mods").get("pager").get("data").get("totalCount")
            auctions = text_json.get("mods").get("itemlist").get("data").get("auctions")
            for auction_index in range(len(auctions)):
                auction = auctions[auction_index]
                item = TaobaocrawlItem()
                item["nid"] = auction.get("nid").strip()
                item["search_word"] = q
                item["title"] = auction.get("raw_title").strip()
                item["pic_url"] = "https:" + auction.get("pic_url").strip()
                item["detail_url"] = "https:" + auction.get("detail_url").strip()
                item["view_price"] = float(auction.get("view_price"))
                item["item_loc"] = auction.get("item_loc").strip()
                view_sales= auction.get("view_sales").strip()
                view_sales_num=re.search(r"\d+(\.\d+)?", view_sales)
                view_sales_num=float(view_sales_num.group())
                if('万' in view_sales):
                    view_sales_num=view_sales_num*10000
                item["view_sales"]= int(view_sales_num)
                item["comment_count"]=auction.get("comment_count","0")
                if(''==item["comment_count"]):
                    item["comment_count"] = 0
                else:
                    item["comment_count"]=int(item["comment_count"])
                item["nick"] = auction.get("nick")
                item["shop_link"] = "https:" + auction.get("shopLink").strip()
                self.add_totalCount(1)
                print(f'爬取[{item["detail_url"]}]的信息成功，目前已爬取共[{self.totalCount}]条数据\n')
                yield item
            if (currentPage < totalPage and currentPage <10):
                s = data_value
                data_value = data_value + pageSize
                t = time.time()
                _ksTS = int(round(t * 1000))
                staobaoz = time.strftime('%Y%m%d', time.localtime(t))
                req_url = f"https://s.taobao.com/search?data-key=s&data-value={data_value}&ajax=true&_ksTS={_ksTS}_1404&q={q}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{staobaoz}&ie=utf8&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s={s}"
                meta = {"q": q, "data_value": data_value}
                req_headers = copy.deepcopy(self.headers)
                req_headers["Referer"] = req_url
                req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
                print(f"准备爬取[{q}]第[{currentPage+1}]页req_url=[{req_url}]的列表信息\n")
                yield Request(url=req_url, method='GET', headers=req_headers, callback=self.pagination_parse, meta=meta,
                              dont_filter=True)

    # 统计总数
    def add_totalCount(self, count):
        self.mutex.acquire()
        self.totalCount += count
        self.mutex.release()
