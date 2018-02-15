# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):

	# 书名
	book_name = scrapy.Field()
	# 出版信息
	info = scrapy.Field()
	# 简介
	intro = scrapy.Field()
	# 评分
	grade = scrapy.Field()
	# 评价人数
	evaluate_number = scrapy.Field()
	# 来源链接
	source_url = scrapy.Field()
	# 来源名称
	source_name = scrapy.Field()
