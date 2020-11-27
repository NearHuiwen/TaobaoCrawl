# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/11/26 16:38




"""
    Cookie_Utils工具类
"""


class Cookie_Utils:
    def __init__(self):
        self.cookie_list = [
                        "登录后复制cookie写在这里"
                            ]
        self.cookie_count = self.getCookie_Count()
        self.cur_pointer = 0

    def getCookieByPoll(self):
        self.cur_pointer += 1
        if (self.cur_pointer == self.cookie_count):
            self.cur_pointer = 0
        return self.getCookieByIndex(self.cur_pointer)

    def getCookie_Count(self):
        return len(self.cookie_list)

    def getCookieByIndex(self, index):
        return self.cookie_list[index]

