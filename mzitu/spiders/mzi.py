# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mzitu.items import MziItem
from scrapy import Request


class MziSpider(CrawlSpider):
    name = 'mzi'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@id="pins"]/li/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(.,"下一页")]'))
    )
    def parse_item(self, response):
        print('url:' + response.url)
        item = MziItem()
        item['title'] = response.xpath('//div[@class="content"]/h2/text()').extract_first()
        item['url'] = response.xpath('//div[@class="main-image"]//img/@src').extract()[0]
        yield item
        next_url = response.xpath('//div[@class="pagenavi"]/a/@href').extract()[-1]
        yield Request(next_url, callback=self.parse_item)
