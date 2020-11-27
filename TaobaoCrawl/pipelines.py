# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from TaobaoCrawl.items import TaobaocrawlItem


class TaobaocrawlPipeline:
    def process_item(self, item, spider):
        if (isinstance(item, TaobaocrawlItem)):
            spider.mysql_utils.replace_good(item)
        return item
