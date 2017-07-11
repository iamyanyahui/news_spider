# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website = scrapy.Field
    url = scrapy.Field
    crawl_time = scrapy.Field
    publish_time = scrapy.Field
    source = scrapy.Field
    source_url = scrapy.Field
    title = scrapy.Field
    author = scrapy.Field
    content = scrapy.Field
    hot = scrapy.Field
    hits = scrapy.Field
    replies = scrapy.Field
#     'website': '天涯博客',
#     'url': url,
#     'crawl_time': datetime.now(),
#     'publish_time': publish_time,  # response.css('div.article-tag.pos-relative.cf span.pos-right.gray6::text').re_first(r'(\d+\-\d+\-\d+\s+\d+:\d+)\s+\w+'),
#     'source': '天涯博客',
#     'source_url': url,
#     'title': response.css('div.content-container h2 a::text').extract_first().strip() or '',
#     'author': response.css('div.headerinner h1 a::text').extract_first()
#     or response.css('div#blogtitle h1 a::text').extract_first(),
#
#
# 'content': self.parse_content(response) or '',
# 'hot': response.xpath('//em[contains(@id, "PostClick")]/text()').extract_first() or 0,
# 'hits': response.css('em#PostClick::text').extract_first() or 0,
# 'replies': response.xpath('//a[@href=$val]/text()', val='#allcomments').re_first(r'评论.(\d+)') or 0,

