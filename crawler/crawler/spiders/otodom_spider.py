# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import CrawlerItem

class GumtreeSpider(CrawlSpider):
    name = "otodom"
    allowed_domains = ["otodom.pl"]
    start_urls = ['http://otodom.pl/index.php?mod=listing&source=context&objSearchQuery.OfferType=rent&objSearchQuery.ObjectName=Flat&objSearchQuery.Country.ID=1&objSearchQuery.Province.ID=&objSearchQuery.District.ID=&objSearchQuery.CityName=&objSearchQuery.QuarterName=&objSearchQuery.StreetName=&objSearchQuery.LatFrom=&objSearchQuery.LatTo=&objSearchQuery.LngFrom=&objSearchQuery.LngTo=&objSearchQuery.PriceFrom=&objSearchQuery.PriceTo=&objSearchQuery.PriceCurrency.ID=1&objSearchQuery.AreaFrom=&objSearchQuery.AreaTo=&objSearchQuery.FlatRoomsNumFrom=&objSearchQuery.FlatRoomsNumTo=&objSearchQuery.FlatFloorFrom=&objSearchQuery.FlatFloorTo=&objSearchQuery.FlatFreeFrom=&objSearchQuery.FlatBuildingType=&objSearchQuery.Heating=&objSearchQuery.BuildingYearFrom=&objSearchQuery.BuildingYearTo=&objSearchQuery.FlatFloorsNoFrom=&objSearchQuery.FlatFloorsNoTo=&objSearchQuery.CreationDate=&objSearchQuery.Description=&objSearchQuery.offerId=&objSearchQuery.Orderby=default&resultsPerPage=25&Search=Search&Location=&currentPage=1'] 
    rules = [Rule(SgmlLinkExtractor(allow=['\currentPage=\d+'], restrict_xpaths=('//a[@class="od-btn od-btn_small od-btn_green od-pagination_next"]')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//h1[@class="od-listing_item-title"]/a')), 'parse_ad', follow=True)]

    def parse_ad(self, response):
        sel = Selector(response)
        ad = CrawlerItem()
        ad['title'] = sel.xpath("//h1[@class='offer-title']/text()").extract()[0]
        ad['url'] = response.url

        # # parsowanie opisu
        description = ""
        for line in sel.xpath("//div[@class='od-offer-description']//text()").extract():
            line = line.strip()
            if not line:
                continue
            description += line + "\n"
        ad['desc'] = description

        ad['date'] = sel.xpath("//p[@class='od-offer-description-meta']//text()").extract()[1]
        ad['price'] = sel.xpath("//td[@class='od-offer-price']//text()").extract()[0].strip()
        ad['area'] = sel.xpath("//td[@class='od-offer-area']//text()").extract()[0].strip()
        ad['rooms'] = sel.xpath("//table[@class='od-offer-numbers clearfix']//text()").extract()[3].strip()

        address = ""
        for line in sel.xpath("//dd[@id='mapTitle']//text()").extract():
            line = line.strip()
            if not line:
                continue
            address += line
        ad['address'] = address
        return ad