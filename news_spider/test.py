# coding: utf8
import urllib
from datetime import datetime

import requests
import urllib3



def test_bbs():
    url = 'http://bbs.tianya.cn/hotArticle.jsp?pn=7'
    r = requests.get(url)
    print(r.text)


if __name__ == '__main__':
    # test_bbs()
    print(datetime.strptime('2017-07-06 16:17:40', '%Y-%m-%d %H:%M:%S'))
