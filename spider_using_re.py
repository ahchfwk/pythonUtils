# -*- coding:utf-8 -*-
'''created by fwk
   2017/9/30
   spider some info from https://github.com/
'''

import urllib
import urllib2
import cookielib
import re

# 保存cookie到文件
cookie = cookielib.MozillaCookieJar('./cookie.txt')
handle = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handle)
opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)

# 从文件获取cookie并加载
cookie = cookielib.MozillaCookieJar()
cookie.load('./cookie.txt', ignore_discard=True, ignore_expires=True)
handle = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handle)
result = opener.open('http://www.baidu.com')
# print result.read()

# 利用cookie模拟网站登陆
'''
cookie = cookielib.MozillaCookieJar('./cookie.txt')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'login_field': '1257558552@qq.com',
    'password': 'fwk18133623380..'
})
loginUrl = 'https://github.com/login/session'
result = opener.open(loginUrl, postdata)
print result.read()
# open操作之后，cookie就已经被保存了，下行是将其保存到文件中
cookie.save(ignore_discard=True, ignore_expires=True)
gradeUrl = 'https://github.com/ahchfwking/hello-github'
result = opener.open(gradeUrl)
print result.read()
'''


def get_commit(url):
    request = urllib2.Request(url+'/commits')
    response = urllib2.urlopen(request)
    # pattern = re.compile(r'class="commit-group-title".*?</svg>(.*?)</div>|table-list-cell".*?title="(.*?)"', re.S)
    pattern1 = re.compile(r'class="commit-group-title".*?</svg>(.*?)</div>', re.S)
    pattern2 = re.compile(r'table-list-cell".*?title="(.*?)"', re.S)
    response = response.read()
    result1 = re.findall(pattern1, response)
    result2 = re.findall(pattern2, response)
    for item in result1:
        print item.strip()
    
    for item in result2:
        print item.strip()

if __name__ == '__main__':
    get_commit('https://github.com/Mondego/SourcererCC')