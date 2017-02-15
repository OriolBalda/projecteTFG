# -*- coding: utf-8 -*-
import scrapy

class HMliniesItem(scrapy.Item):
    name = scrapy.Field()
    parent = scrapy.Field()
    link = scrapy.Field()
    
class HMproductesItem(scrapy.Item):
    name = scrapy.Field()
    
