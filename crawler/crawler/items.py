# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
    title = Field()
    desc = Field()
    date = Field()
    price = Field()
    address = Field()
    rooms = Field()
    area = Field()
    url = Field()
