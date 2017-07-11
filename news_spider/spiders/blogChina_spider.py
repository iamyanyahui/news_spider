# coding: utf-8
import requests
import scrapy
from process_html import filter_tags
from datetime import datetime
import time


class BlogChinaSpider(scrapy.Spider):
    name = 'blog_china'
    # start_urls = [
    #     'http://tuijian.blogchina.com/list/index/flag/2/channel/1/page/10'
    # ]

    def start_requests(self):
        original_url = 'http://tuijian.blogchina.com/list/index/flag/2/channel/1/page/'
        start_urls = []
        for i in range(1,11):
            start_urls.append(original_url + str(i))
        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        urls = response.css('li.tit_a a::attr(href)').extract()[::2]
        for url in urls:
            yield response.follow(url=url, callback=self.parse_blog)
        # yield response.follow(url='http://bokekeji.blogchina.com/608325693.html', callback=self.parse_blog)

    def parse_blog(self, response):
        article = response.css('div.article').extract_first()
        content = filter_tags(article).replace(u'\xa0', u'').replace(u'\u3000', u'')
        info = response.css('div.article div.editable p').extract()[0:2]
        author = response.css('div.avatar-name a::text').extract_first() or ''
        if author:
            author = author.strip()

        source = '博客中国'
        filter_info = [filter_tags(x).strip() for x in info]
        flag_author = False
        flag_source = False
        if filter_info[0].startswith('作者') or filter_info[0].startswith('撰文'):
            author = filter_info[0][3:]
            flag_author = True
        if filter_info[0].startswith('来源'):
            source = filter_info[0][3:]
            flag_source = True
        if (not flag_source) and filter_info[1].startswith('来源'):
            source = filter_info[1][3:]
        if (not flag_author) and filter_info[1].startswith('作者') or filter_info[1].startswith('撰文'):
            author = filter_info[1][3:]

        website = '博客中国'
        url = response.url
        crawl_time = datetime.now()
        title = response.css('div.d_testbox::text').extract_first() or ''
        p_time = response.css('span.time::text').extract_first() or ''
        publish_time = crawl_time
        if p_time:
            p_time = p_time.lstrip().rstrip()
            publish_time = datetime.strptime(p_time, '%Y-%m-%d %H:%M:%S')
        hits = self.get_browse_count(response)
        replies = response.css('ul.num_hot').re_first('<li><i class="fa fa-comment-o"></i>(\d+)</li>') or 0

        yield {
            'website': website,
            'url': url,
            'crawl_time': crawl_time,
            'publish_time': publish_time,
            'source': source,
            'source_url': url,
            'title': title,
            'author': author,
            'content': content,
            'hot': hits,
            'hits': hits,
            'replies': replies,
        }

    def get_browse_count(self, response):
        browse_count_original_url = 'http://post.blogchina.com/addBrowseCount'
        aid = response.xpath('//input[@id="aid"]/@value').extract_first()
        user_id = response.xpath('//input[@id="user_id"]/@value').extract_first()
        if aid and user_id:
            url = browse_count_original_url + '?aid=' + str(aid) + \
                  '&user_id=' + str(user_id) + '&type=click&incr=y&_=' + str(int(round(time.time() * 1000)))
            r = requests.get(url)
            num = eval(r.text)['data']['num']
            return num
        else:
            return 0

