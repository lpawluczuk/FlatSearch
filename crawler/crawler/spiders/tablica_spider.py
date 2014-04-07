# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

import re

class TablicaSpider(CrawlSpider):
    name = "tablica"
    allowed_domains = ["tablica.pl"]
    start_urls = ['http://tablica.pl/nieruchomosci/mieszkania/wynajem/?page=1'] 
    rules = [Rule(SgmlLinkExtractor(allow=['\?page=\d+'], restrict_xpaths=('//span[@class="fbold next abs large"]/a')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="link linkWithHash detailsLink {clickerID:\'ads_title\'}"]')), 'parse_ad', follow=True)]

    def parse_ad(self, response):
        sel = Selector(response)
        ad = CrawlerItem()
        ad['title'] = sel.xpath("//div[@class='clr offerheadinner pding15']/h1/text()").extract()[0].strip()
        ad['url'] = response.url

        # # parsowanie opisu
        description = ""
        for line in sel.xpath("//div[@id='textContent']//text()").extract():
            line = line.strip()
            if not line:
                continue
            description += line + "\n"
        ad['desc'] = description
        ad['address'] = sel.xpath("//div[@class='address fleft marginleft15']//p//text()").extract()[0].strip()
        ad['price'] = sel.xpath("//strong[@class='xxxx-large margintop7 block not-arranged']//text()").extract()[0].strip()
        ad['date'] = re.sub('\s+', ' ', sel.xpath("//span[@class='pdingleft10 brlefte5']//text()").extract()[0].strip())
        
        attributes = sel.xpath("//tr[@class='brbottdashc8']//text()").extract()
        attributes = filter(lambda a: a, [attr.strip() for attr in attributes])

        # parsowanie niepodpisanej tabeli
        for i in range(len(attributes)):
            if "pokoi" in attributes[i]:
                ad['rooms'] = attributes[i+1].strip()
            elif "Powierzchnia" in attributes[i]:
                ad['area'] = attributes[i+1].strip()
        return ad
