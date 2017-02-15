# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
import re
import unicodedata
from crawlHM.items import HMliniesItem

def isNumber(s):
    if re.match("^\d+?\.\d+?$", s) is None:
        return False
    return True

def obtainName(w):
    w = w.replace('\t','')
    w = w.replace('\r','')
    w = w.replace('\n','')
    wordlist = w.split(' ')
    name = ''
    for word in wordlist:
        if len(word) != 0:
            name = name + word + ' '
    unicodedata.normalize('NFKD', name).encode('ascii','ignore')
    return name[:-1]

class HmliniesSpider(scrapy.Spider):
    name = "HMlinies"
    allowed_domains = ["www2.hm.com"]
    start_urls = ['http://www2.hm.com/es_es/index.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlHM.pipelines.HMliniesPipeline': 300 # L'enter defineix l'ordre en el que s'executen els pipelines (abans == més baix)
        }
    }

    def parse(self, response):
        hxs = scrapy.Selector(response,type='html')
        primary_menu = hxs.xpath("//nav[@class='primary-menu']/*")[0]
        list_menu = primary_menu.xpath('./*')
        for item_menu in list_menu:
            unicode_name = item_menu.css('a::text').extract_first()
            unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
            name = unicode_name.encode('utf-8')
            link = item_menu.css('a::attr("href")').extract_first()
            itemLoader = ItemLoader(item=HMliniesItem(), response=response)
            itemLoader.add_value('name', name)
            itemLoader.add_value('parent',0)
            itemLoader.add_value('link',link)
            yield itemLoader.load_item()
            yield scrapy.Request(response.urljoin(link) , callback=self.parse_linies, meta={'parent': name})

    def parse_linies(self, response):
        parent = response.meta['parent']
        hxs = scrapy.Selector(response, type='html')
        section_menu_categories = hxs.xpath("//div[@class='section-menu-categories']")
        if (len(section_menu_categories) != 0):
            list_category = section_menu_categories[0].xpath('./div')
            b = False;
            for item_category in list_category:
                containsProducts = len(item_category.xpath('./h4/span[contains(text(),"Compra por producto")]')) != 0
                if containsProducts:
                    b = True;
                    productLines = item_category
                    break
            if (b):
                list_productLines = productLines.xpath('.//li[@class="section-menu-subdepartment "]')
                for item_productLines in list_productLines:
                    unicode_name = obtainName(item_productLines.xpath('.//a/text()').extract_first())
                    unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
                    name = unicode_name.encode('utf-8')
                    link = item_productLines.xpath('.//a/@href').extract_first()
                    itemLoader = ItemLoader(item=HMliniesItem(), response=response)
                    itemLoader.add_value('name', name)
                    itemLoader.add_value('parent',parent)
                    itemLoader.add_value('link',link)
                    yield itemLoader.load_item()
                    yield scrapy.Request(response.urljoin(link) , callback=self.parse_linies2, meta={'gparent': parent, 'parent': name})
                    
    def parse_linies2(self, response):
        gparent = response.meta['gparent']
        parent = response.meta['parent']
        hxs = scrapy.Selector(response, type='html')
        linia = hxs.xpath('//li[@class="section-menu-subdepartment current"]')[0]
        list_sublinies = linia.xpath('.//li[@class="section-menu-subcategory "]')
        for item_sublinies in list_sublinies:
            unicode_name = obtainName(item_sublinies.xpath('.//a/text()').extract_first())
            unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
            name = unicode_name.encode('utf-8')
            link = item_sublinies.xpath('.//a/@href').extract_first()
            itemLoader = ItemLoader(item=HMliniesItem(), response=response)
            itemLoader.add_value('name', name)
            itemLoader.add_value('parent',gparent+'_'+parent)
            itemLoader.add_value('link',link)
            yield itemLoader.load_item()
            
        
        