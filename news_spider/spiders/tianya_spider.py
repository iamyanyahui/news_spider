# coding:utf8
from datetime import datetime
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from process_html import filter_tags



class BlogSpider(scrapy.Spider):
    name = 'tianya_blog'

    def start_requests(self):
        urls = [
            'http://blog.tianya.cn',
            'http://focus.tianya.cn/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for href in response.css('div.mulit-column.mulit-column-not-h-last.mulit-column-not-v-last a[desc*=标题]::attr(href)').extract():
            # print(href)
            yield response.follow(href, callback=self.parse_blog)

    def parse_blog(self, response):
        url = response.url
        time = response.css('div.article-tag.pos-relative.cf span.pos-right.gray6::text').re_first(r'(\d+\-\d+\-\d+\s+\d+:\d+)\s+\w+')
        publish_time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        yield {
            'website': '天涯博客',
            'url': url,
            'crawl_time': datetime.now(),
            'publish_time': publish_time, #response.css('div.article-tag.pos-relative.cf span.pos-right.gray6::text').re_first(r'(\d+\-\d+\-\d+\s+\d+:\d+)\s+\w+'),
            'source': '天涯博客',
            'source_url': url,
            'title': response.css('div.content-container h2 a::text').extract_first().strip() or '',
            'author': response.css('div.headerinner h1 a::text').extract_first()
                      or response.css('div#blogtitle h1 a::text').extract_first(),
            'content': self.parse_content(response) or '',
            'hot': response.xpath('//em[contains(@id, "PostClick")]/text()').extract_first() or 0,
            'hits': response.css('em#PostClick::text').extract_first() or 0,
            'replies': response.xpath('//a[@href=$val]/text()', val='#allcomments').re_first(r'评论.(\d+)') or 0,
        }

    def parse_content(self, response):
        content = response.css('p::text').extract() or response.css('p span::text').extract()
        string = ""
        for p in content:
            string += p.rstrip()
        return string


class BbsSpider(CrawlSpider):
    name = 'tianya_bbs'

    def start_requests(self):
        start_urls = [
            'http://bbs.tianya.cn/hotArticle.jsp?pn=1',
            'http://focus.tianya.cn/'
        ]
        yield scrapy.Request(url=start_urls[0], callback=self.parse)
        yield scrapy.Request(url=start_urls[1], callback=self.parse_bbs_area)

    def parse(self, response):
        for href in response.css('table td.td-title a::attr(href)').extract():
            # print(href)
            yield response.follow(href, callback=self.parse_bbs)

        next_page = response.css('div[class*=long-pages] a')[-1]
        if next_page.css('a::text').extract_first() == '下页':
            yield response.follow(next_page.css('a::attr(href)').extract_first(), callback=self.parse)

        # href = response.css('table td.td-title a::attr(href)').extract_first()
        # yield response.follow(href, callback=self.parse_bbs)

    def parse_bbs(self, response):
        url = response.url
        author_wraper = response.css('div.atl-menu.clearfix.js-bbs-act div.atl-info span')
        # print(author_wraper)
        author = author_wraper[0].css('a::text').extract_first().strip()

        header_info = response.css('div.atl-menu.clearfix.js-bbs-act div.atl-info span::text').extract()
        time = header_info[1].rstrip()[3:]#header_info[1].css('span::text').extract_first().rstrip()[3:]#[3:22]
        publish_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        hits = header_info[2].strip()[3:] #header_info[2].css('span::text').extract_first().strip()[3:]
        replies = header_info[3].strip()[3:] #header_info[3].css('span::text').extract_first().strip()[3:]

        content = response.css('div.bbs-content.clearfix').extract_first() or ''
        if content:
            content = filter_tags(content).replace(u'\xa0', u'').replace(u'\u3000', u'')

        yield {
            'website': '天涯论坛',
            'url': url,
            'crawl_time': datetime.now(),
            'publish_time': publish_time,
            'source': '天涯论坛',
            'source_url': url,
            'title': response.css('div[id*=post_head] span::text').extract_first(),
            'author': author,
            'content': content,
            'hot': hits,
            'hits': hits,
            'replies': replies,
        }

    def parse_bbs_topic(self, response):
        for href in response.xpath('//a[@desc=$val]/@href', val="标题").extract():
            if (href[7:10] == 'bbs') and ('post' in href):
                yield response.follow(href, callback=self.parse_bbs)

    def parse_bbs_area(self, response):
        for url in response.css('ul.bbs-area.fl a::attr(href)').extract():
            yield response.follow(url, callback=self.parse_bbs_topic)
