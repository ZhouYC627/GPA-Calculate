#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import sys
import os
import getpass
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

filename = 'cookie.txt'
StudentID = '141220162'
Password = '450283'
#StudentID = raw_input("Student ID: ")
#Password = getpass.getpass("Password:  ")
os.system("cls") # windows
os.system("clear") # linux

#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
            'userName':StudentID,
            'password':Password
        })
#登录教务系统的URL
loginUrl = 'http://jwas3.nju.edu.cn:8080/jiaowu/login.do'
#模拟登录，并把cookie保存到变量
result = opener.open(loginUrl, postdata)
#保存cookie到cookie.txt中
cookie.save(ignore_discard=True, ignore_expires=True)
#利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://jwas3.nju.edu.cn:8080/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList'
#请求访问成绩查询网址
result = opener.open(gradeUrl)
html = result.read().decode('utf-8')

soup = BeautifulSoup(html, "lxml")

items = []
flag = False
for string in soup.stripped_strings:
    if string == "学分统计".encode('utf-8'):
        flag = True
        continue
    if flag:
        if string.find("注：".encode('utf-8')) != -1:
            break
        items.append(string.encode('utf-8'))

print ("%30s"%(items[0]))
#成绩结果输出对齐
def myAlign(string, length=0):
	if length == 0:
		return string
	slen = len(string)
	re = string
	if isinstance(string, str):
		placeholder = ' '
	else:
		placeholder = u'　'
	while slen < length:
		re += placeholder
		slen += 1
	return re

#学分绩计算
i=15
sum = 0.0
weight = 0.0
while i<len(items):
    #print ("%d %-20s\t%-5s\t%-8s"%(i/7-1, items[i-3], items[i], items[i+1]))
    print (i/7-1), myAlign(items[i-3], 20)+"\t"+myAlign(items[i],5), items[i+1]
    sum += float(items[i])*float(items[i+1])
    weight += float(items[i])
    i+=7

print ("\nGPA:") ,sum/weight/20
os.remove(filename)
