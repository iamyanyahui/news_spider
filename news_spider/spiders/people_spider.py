# coding: utf8
from datetime import datetime
import scrapy
from process_html import filter_tags
import requests


# 爬取人民网论坛的内容
class PeopleSpider(scrapy.Spider):
    name = 'people_bbs'

    def start_requests(self):
        start_urls = [
            'http://bbs1.people.com.cn/',
        ]
        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        topic_urls = response.css('div.nav_bottom.clearfix a::attr(href)').extract()

        for url in topic_urls:
            yield response.follow(url=url, callback=self.parse_topic_bbs_list)

    def parse_topic_bbs_list(self, response):
        urls = response.css('ul.replayList p.treeTitle a.treeReply::attr(href)').extract()
        for url in urls:
            yield response.follow(url=url, callback=self.parse_bbs)

    def parse_bbs(self, response):
        article_path = response.css('div.article.scrollFlag::attr(content_path)').extract_first()
        content = ''
        if article_path:
            content = self.get_content(article_path).replace(u'\xa0', u'').replace(u'\u3000', u'')

        title = response.css('title::text').extract_first() or ''
        if (not content) and title:
            content = title

        author = response.css('a.float_l.userNick font::text').extract_first()
        replay_info_selector = response.css('p.replayInfo')
        hits = replay_info_selector.css('span.readNum::text').extract_first()
        replies = replay_info_selector.css('span.replayNum::text').extract_first()
        time = replay_info_selector.re_first(r'(\d+\-\d+\-\d+\s*\d+:\d+:\d+)</span>')
        publish_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        crawl_time = datetime.now()
        url = response.url
        website = '人民网'

        yield {
            'website': website,
            'url': url,
            'crawl_time': crawl_time,
            'publish_time': publish_time,
            'source': website,
            'source_url': url,
            'title': title,
            'author': author,
            'content': content,
            'hot': hits,
            'hits': hits,
            'replies': replies,
        }

    def get_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            content = str(response.content, encoding='utf-8')
            content = filter_tags(content)
            return content
        else:
            return ''


