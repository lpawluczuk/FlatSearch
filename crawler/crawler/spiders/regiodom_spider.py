# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

import re

class RegiodomSpider(CrawlSpider):
    name = "regiodom"
    allowed_domains = ["regiodom.pl"]
    start_urls = ['http://regiodom.pl/cala_polska/mieszkania-do-wynajecia-rynek-wtorny,1,1,50,cur,page,on_page'] 
    rules = [ Rule(SgmlLinkExtractor(allow=['1,\d+,50,cur,page,on_page'], restrict_xpaths=('//a[@class="next"]')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="imgLink"]')), 'parse_ad', follow=True)]

    def parse_ad(self, response):
        sel = Selector(response)
        ad = CrawlerItem()
        ad['title'] = sel.xpath("//h1[@class='advHeader']/text()").extract()[0]
        ad['url'] = response.url

        # parsowanie opisu
        description = ""
        for line in sel.xpath("//div[@id='description']//text()").extract():
            line = line.strip()
            if not line:
                continue
            description += line + "\n"
        ad['desc'] = description

        ad['date'] = re.sub(r'data dodania\:', r'', sel.xpath("//p[@class='grayHeaderText']//span//text()").extract()[0]).strip()
        ad['price'] = sel.xpath("//p[@id='priceDetailsH3']//text()").extract()[0].strip()


        offerDetails = sel.xpath("//div[@class='detail']//dd//text()").extract()
        
        ad['area'] = offerDetails[12].strip()
        ad['rooms'] = offerDetails[15].strip()

        ad['address'] = ', '.join([x.strip() for x in offerDetails[3:10] if x.strip()])
        return ad