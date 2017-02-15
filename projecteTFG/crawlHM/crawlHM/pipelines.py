# -*- coding: utf-8 -*-
from twisted.protocols.dict import DictLookup
import json

class HMliniesPipeline(object):
    
    dictLinies = {}
    ruta_dictLinies = 'data\linies_hm.json'
    
    def open_spider(self, spider):
        HMliniesPipeline.dictLinies = {}
    
    def process_item(self, item, spider):
        name = item['name'][0]
        parent = item['parent'][0]
        link = item['link'][0]
        if parent == 0:
            HMliniesPipeline.dictLinies[name] = ({},link)
        else:
            list_parent = parent.split('_')
            if len(list_parent) == 1:
                HMliniesPipeline.dictLinies[parent][0][name] = ({},link)
            else:
                HMliniesPipeline.dictLinies[list_parent[0]][0][list_parent[1]][0][name] = link
        return item
    
    def close_spider(self, spider):
        with open(HMliniesPipeline.ruta_dictLinies, 'w') as f:
            json.dump(HMliniesPipeline.dictLinies,f)
        pass
        
class HMproductesPipeline(object):
    
    def open_spider(self, spider):
        pass
    
    def process_item(self, item, spider):
        return item
    
    def close_spider(self, sider):
        pass
