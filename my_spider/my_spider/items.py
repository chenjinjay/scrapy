# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanMovieItem(scrapy.Item):

    ranking = scrapy.Field()           # 排名
    movie_name = scrapy.Field()        # 名称 
    score = scrapy.Field()             # 评分
    score_num = scrapy.Field()        # 评论数
