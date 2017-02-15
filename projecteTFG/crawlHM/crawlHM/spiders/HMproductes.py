# -*- coding: utf-8 -*-
import scrapy


class HmproductesSpider(scrapy.Spider):
    name = "HMproductes"
    allowed_domains = ["www2.hm.com"]
    #start_urls = ['http://www2.hm.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'app.HMproductesPipeline': 300
        }
    }

    def parse(self, response):
        pass
