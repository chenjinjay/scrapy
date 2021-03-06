# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
from scrapy.crawler import Settings as settings
import copy

class jsondouban_pipline(object):         # 1、在settings.py文件中配置 2、在自己实现的爬虫类中yield item,会自动执行
    def __init__(self):
        self.file = codecs.open('info.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()


class douban_pipline(object):            # 把数据存到mysql的类

    def __init__(self,dbpool):             # dbpool是 from_setting 下面得到的
        self.dbpool=dbpool

    @classmethod                           # 类方法，无需实例化就可以调用
    def from_settings(cls,settings):        # 名称固定 会被scrapy调用 直接可用setting的值 
        dbparams=dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams) #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)


    def process_item(self,item,spider):       # process_item方法是pipeline默认调用的，进行数据库操作
        asynItem = copy.deepcopy(item)
        query=self.dbpool.runInteraction(self._conditional_insert,asynItem)   #调用插入的方法 Interaction(中文是交互)
        query.addErrback(self._handle_error,asynItem,spider)                  #调用异常处理方法
        return asynItem        

    def _conditional_insert(self,tx,item):
        sql="insert into result(ranking,movie_name,score,score_num) values(%s,%s,%s,%s)"
        params=(item["ranking"],item["movie_name"],item["score"],item["score_num"])
        tx.execute(sql,params)
    def _handle_error(self, failue, item, spider):
        print (failue)


