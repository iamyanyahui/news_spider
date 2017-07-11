# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem

from news_spider import settings


def db_handle():
    conn = pymysql.connect(**settings.DATABASES)
    return conn


class NewsSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def process_item(self, item, spider):
        if item['content'] and (item['crawl_time']-item['publish_time']).days <= 10:
            db_object = db_handle()
            cursor = db_object.cursor()
            sql = 'insert into news(website, url, crawl_time, publish_time, source, source_url, title, author, content, hot, hits, replies) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor.execute(sql,
                               (item['website'], item['url'], item['crawl_time'], item['publish_time'], item['source'], item['source_url'], item['title'], item['author'], item['content'], item['hot'], item['hits'], item['replies']))
                db_object.commit()
            except Exception as e:
                print(e)
                db_object.rollback()
            finally:
                db_object.close()
            return item
        else:
            raise DropItem('no content in this item: %s', item)
