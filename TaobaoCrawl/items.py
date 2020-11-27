# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaocrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nid= scrapy.Field()#商品ID
    search_word= scrapy.Field()#搜索词
    title = scrapy.Field()#商品标题
    pic_url = scrapy.Field()#简介图片
    detail_url = scrapy.Field()#商品详情网站地址
    view_price = scrapy.Field()#商品价格（最低价）
    item_loc = scrapy.Field()#商品来源地市
    view_sales = scrapy.Field()#已有多少个人收到货
    comment_count =scrapy.Field()#积累评论数
    nick = scrapy.Field()#商家名称
    shop_link =scrapy.Field()#商铺网站地址
