# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

import re

class MorizonSpider(CrawlSpider):
    name = "morizon"
    allowed_domains = ["morizon.pl"]
    start_urls = ['http://www.morizon.pl/289/mieszkania/wynajem.html?page=1', 'http://www.morizon.pl/192/domy/wynajem.html?page=1'] 
    rules = [ Rule(SgmlLinkExtractor(allow=['\page=\d+'], restrict_xpaths=('//a[@rel="next"]')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="offer"]//h3//a')), 'parse_ad', follow=True)]

    def parse_ad(self, response):
        sel = Selector(response)
        ad = CrawlerItem()
        ad['title'] = sel.xpath("//h1[@class='offerTitle']/text()").extract()[0]
        ad['url'] = response.url

        # parsowanie opisu
        description = ""
        for line in sel.xpath("//div[@class='offerDescription']//text()").extract():
            line = line.strip()
            if not line:
                continue
            description += line + "\n"
        ad['desc'] = description

        ad['date'] = "" #tu nie ma daty!

        offerDetails = sel.xpath("//div[@class='offerDetails']//text()").extract()

        ad['price'] = offerDetails[3].strip()
        ad['area'] = offerDetails[14].strip()
        ad['rooms'] = offerDetails[33].strip()

        address = ad['title']

        address = re.sub(r'Dom\,?', r'', address)
        address = re.sub(r'Mieszkanie\,?', r'', address)
        address = re.sub(r'\,[0-9]{1,5}m.', r'', address)
        ad['address'] = address.strip()
        return ad