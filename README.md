# news_spider
scrapy小爬虫
共有三个小爬虫，分别爬取人民网bbs、天涯bbs和天涯blog、博客中国，爬取十天之内的数据。
获取的信息整合为：
website ֦网站
url 博客或bbs的url
crawl_time 爬取时间
publish_time 内容发布时间
source 来源
source_url ܻ来源的url
title 标题
author 作者
content 内容
hot 热度（通常为点击或查看的次数）
hits 点击数（查看数）
replies 回复数

三个爬虫加起来，每次爬取的数据大概有一千条。
