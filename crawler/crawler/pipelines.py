# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# ten kod dobrze exportuje do JSON'a z utf-8, ale nie zrzuca tablicy JSON'ow tylko obiekty po kolei
# import json
# import codecs

# class CrawlerPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
#         self.file.write(line)
#         return item

#     def spider_closed(self, spider):
#         self.file.close()


from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter

class CrawlerPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file, indent=4) # tu powinno byc ensure_ascii=False ale nie dziala;P
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item