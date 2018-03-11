# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests

print('请选择学期:84=2015-2016 1, 103=2015-2016 2, 123=2016-2017 1, 143=2016-2017 2')
semester = input()
url = 'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=' + str(semester)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Host' : 'idas.uestc.edu.cn',
			'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Referer' : 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal',
			'Content-Type' : 'application/x-www-form-urlencoded'
}
cookie = {
	'semester.id' : '143',
	'JSESSIONID' : 'E6D5780C1DF33641EDAF1DD76A17DDE6',
	'__utma' : '108824541.1860555578.1501034789.1501037549.1501120837.3',
	'__utmz' : '108824541.1501120837.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
	'__utmb' : '108824541.6.10.1501120837',
	'__utmc' : '108824541',
	'iPlanetDirectoryPro' : 'AQIC5wM2LY4SfcxakYHZN1PW0+DNUB9LixMu+ve877ZWQxM=@AAJTSQACMDE=#',
	'__utmt' : '1'
}

r = requests.get(url, headers = headers, cookies = cookie)
s = BeautifulSoup(r.text, 'lxml')
try:
	trs = s.find('tbody').find_all('tr')
except:
	print('cookies失效')
print('学年学期'.ljust(16), '课程名称'.ljust(32), '学分'.ljust(20), '最终'.ljust(15), '绩点'.ljust(15))

try:
	for tr in trs:
		try:
			tds = tr.find_all('td')
		except:
			print('cookies失效')
		i = 1
		for td in tds:
			if i == 1:
				print(td.string.strip().ljust(20), end = '')
			elif i == 4:
				n = 20 - len(td.string.strip())
				print(td.string.strip(), end = ''.ljust(2 * n))
			elif i == 6:
				print(td.string.strip().ljust(20), end = '')
			elif i == 9:
				print(td.string.strip().ljust(20), end = '')
			elif i == 10:
				print(td.string.strip().ljust(20), end = '')
			i += 1
		print('\n')
except:
	print('cookies失效')