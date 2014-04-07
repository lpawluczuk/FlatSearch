# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

class GumtreeSpider(CrawlSpider):
    name = "gumtree"
    allowed_domains = ["gumtree.pl"]
    start_urls = ['http://www.gumtree.pl/fp-mieszkania-i-domy-do-wynajecia/c9008?AdType=2&Page=1'] 
    rules = [Rule(SgmlLinkExtractor(allow=['\?Page=\d+'], restrict_xpaths=('//a[@class="prevNextLink"]')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="ar-title"]')), 'parse_ad', follow=True)]

    def parse_ad(self, response):
        sel = Selector(response)
        ad = CrawlerItem()
        ad['title'] = sel.xpath("//h1[@id='preview-local-title']/text()").extract()[1] #.encode('utf-8').encode('string_escape')
        ad['url'] = response.url

        # parsowanie opisu
        description = ""
        for line in sel.xpath("//span[@id='preview-local-desc']//text()").extract():
            line = line.strip()
            if not line:
                continue
            description += line + "\n"
        ad['desc'] = description

        attributes = sel.xpath("//table[@id='attributeTable']/tbody/tr/td/text()").extract()
        attributes = filter(lambda a: a != '\r\n', attributes)

        # parsowanie niepodpisanej tabeli
        for i in range(len(attributes)):
            if "Data dodania" in attributes[i]:
                
                ad['date'] = attributes[i+1].strip()
            elif "Cena" in attributes[i]:
                ad['price'] = attributes[i+1].strip()
            elif "Adres" in attributes[i]:
                ad['address'] = attributes[i+1].strip()
            elif "pokoi" in attributes[i]:
                ad['rooms'] = attributes[i+1].strip()
            elif "Wielko" in attributes[i]:
                ad['area'] = attributes[i+1].strip()
        return ad