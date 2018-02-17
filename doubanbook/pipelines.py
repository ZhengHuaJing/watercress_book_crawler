# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class DoubanbookPipeline(object):

	def __init__(self):
		# 从配置文件中读取信息
		host = settings['MONGODB_HOST']
		port = settings['MONGODB_PORT']
		db_name = settings['MONGODB_DBNAME']
		sheet_name = settings['MONGODB_SHEETNAME']

		# 创建数据库链接
		client = pymongo.MongoClient(host = host, port = port)
		# 指定数据库名
		mdb = client[db_name]
		# 指定表名
		self.sheet = mdb[sheet_name]

	def process_item(self, item, spider):
		# 如果书名不为NULL则写入数据库
		if item['book_name'] != 'NULL':
			self.sheet.insert(dict(item))
			
			return item