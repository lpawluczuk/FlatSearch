# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

import re

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
                ad['date'] = re.sub('\r\n', '', attributes[i+1])
            elif "Cena" in attributes[i]:
                ad['price'] = re.sub('\r\n', '', attributes[i+1])
            elif "Adres" in attributes[i]:
                ad['address'] = re.sub('\r\n', '', attributes[i+1])
            elif "pokoi" in attributes[i]:
                ad['rooms'] = re.sub('\r\n', '', attributes[i+1])
            elif "Wielko" in attributes[i]:
                ad['area'] = re.sub('\r\n', '', attributes[i+1])
        return ad