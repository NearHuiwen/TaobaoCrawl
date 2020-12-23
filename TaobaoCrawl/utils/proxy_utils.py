# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/11/26 16:38


"""
    Proxy_Utils工具类
"""
import time

import grequests
import requests
from lxml import etree
# from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout

from threading import Lock
class Proxy_Utils:
    def __init__(self, test_url=None, test_headers=None,test_req_type="get"):
        self.proxy_list = [
            "",
        ]
        self.mutex = Lock()
        self.proxy_count = self.getProxy_Count()
        self.cur_pointer = 0
        self.test_url = test_url
        self.test_headers = test_headers
        self.test_req_type=test_req_type

    def getProxyByPoll(self):
        self.mutex.acquire()
        self.cur_pointer += 1
        if (self.cur_pointer == self.proxy_count):
            self.cur_pointer = 0
        proxy=self.getProxyByIndex(self.cur_pointer)
        self.mutex.release()
        return proxy

    def rmProxyByValue(self,value):
        self.mutex.acquire()
        if(value in self.proxy_list):
            self.proxy_list.remove(value)
            self.proxy_count = self.getProxy_Count()
            self.cur_pointer = 0
        self.mutex.release()
        return self.proxy_list


    def getProxy_Count(self):
        return len(self.proxy_list)

    def getProxyByIndex(self, index):
        return self.proxy_list[index]


    def proxy_ip_sp(self):
        self.mutex.acquire()
        for index in range(1, 3):
            req_url = f"http://www.xiladaili.com/gaoni/{index}/"
            _time=int(round(time.time()))
            headers = {
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie':f'Hm_lvt_9bfa8deaeafc6083c5e4683d7892f23d={_time}; Hm_lpvt_9bfa8deaeafc6083c5e4683d7892f23d={_time}',
                    }

            res = requests.get(url=req_url,headers=headers)
            html_etree = etree.HTML(res.text, etree.HTMLParser())
            tr_list = html_etree.xpath("//table[@class='fl-table']/tbody/tr")
            reqs = []
            for tr_index in range(len(tr_list)):
                tr_item = tr_list[tr_index]
                # 响应速度
                response_speed = float(tr_item.xpath("./td[5]/text()")[0].strip())

                if (response_speed < 2):
                    # 代理IP
                    proxy_ip = tr_item.xpath("./td[1]/text()")[0].strip()
                    # 代理协议
                    agency_agreement = tr_item.xpath("./td[2]/text()")[0].strip()
                    # # IP匿名度
                    # ip_anonymity=tr_item.xpath("./td[3]/text()")[0].strip()
                    # # 存活时间
                    # survival_time=tr_item.xpath("./td[6]/text()")[0].strip()

                    if ("HTTPS" not in agency_agreement and "https://" in self.test_url):
                        print(f"代理[{proxy_ip}]无法代理[{self.test_url}]，忽略该代理")
                        continue

                    if ("HTTPS" in agency_agreement):
                        proxy_item = "https://" + proxy_ip
                    else:
                        proxy_item = "http://" + proxy_ip

                    if ("https://" in self.test_url):
                        proxies = {'https': proxy_item}
                    else:
                        proxies = {'http': proxy_item}
                    if("get"==self.test_req_type):
                        reqs.append(grequests.get(self.test_url,headers=self.test_headers, proxies=proxies, verify=False,timeout=(1, 1)))
                    else:
                        reqs.append(grequests.post(self.test_url,headers=self.test_headers, proxies=proxies, verify=False,timeout=(1, 1)))
                    # try:
                    #      res = requests.get(self.test_url, headers=self.test_headers, proxies=proxies, verify=False,timeout=(2, 2))  # verify是否验证服务器的SSL证书
                    #      self.proxy_list.append(proxy_item)
                    #      print(f"代理[{proxies}]使用代理成功，插入代理")
                    # except:
                    #     print(f"代理[{proxies}]使用代理错误，忽略该代理")
                    # except ProxyError as e:
                    #     print(f"代理[{proxies}]使用代理错误，忽略该代理")
                    # except ConnectionError as e:
                    #     print(f"代理[{proxies}]使用代理连接错误，忽略该代理")
                    # except ConnectTimeout as e:
                    #     print(f"代理[{proxies}]使用代理连接超时，忽略该代理")
                    # except ReadTimeout as e:
                    #     print(f"代理[{proxies}]使用代理读出超时，忽略该代理")

            res_list = grequests.map(reqs, size=10)
            for res_index in range(len(res_list)):
                res_item=res_list[res_index]
                if(res_item):
                    for proxy_str in res_item.connection.proxy_manager.keys():
                             self.proxy_list.append(proxy_str)
                             print(f"代理[{proxy_str}]使用代理成功，插入代理")

        self.proxy_count = self.getProxy_Count()
        self.cur_pointer = 0
        self.mutex.release()
        return self.proxy_list

# if __name__ == '__main__':
#     url = 'https://wq.jd.com/commodity/comment/getcommentlist?callback=skuJDEvalA&version=v2&pagesize=10&sceneval=2&score=0&sku=100005094442&sorttype=5&page=1&t=0.38496580237454237'
#
#     headers = {
#         'Connection': 'keep-alive',
#         'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
#         'sec-ch-ua-mobile': '?1',
#         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36',
#         'Accept': '*/*',
#         'Sec-Fetch-Site': 'same-site',
#         'Sec-Fetch-Mode': 'no-cors',
#         'Sec-Fetch-Dest': 'script',
#         'Referer': 'https://item.m.jd.com/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     }
#     proxy_utils = Proxy_Utils(test_url=url, test_headers=headers,test_req_type="get")
#     aaa = proxy_utils.proxy_ip_sp()
