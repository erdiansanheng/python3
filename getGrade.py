from bs4 import BeautifulSoup
import requests
import os

se = requests.Session()

class GetGrade():
	def __init__(self):
		self.url_login = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/logout.portal'
		self.url = 'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=143'
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Referer' : 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
		}
		self.username = '2015220901024'
		self.password = 'landi19970325'
		self.lt = []
		self.dllt = 'userNamePasswordLogin'
		self.execution = []
		self.eventId = 'submit'
		self.rmShown = '1'

	def login(self):
		html = se.get(self.url_login, headers = self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		data = soup.find('form', id = 'casLoginForm').find_all('input')
		for input in data:
			if input.get('name') == 'lt':
				self.lt = input.get('value')
			if input.get('name') == 'execution':
				self.execution = input.get('value')
		login_data = {
			'username' : self.username,
			'password' : self.password,
			'lt' : self.lt,
			'dllt' : self.dllt,
			'execution' : self.execution,
			'-eventId' : self.eventId,
			'rmShown' : self.rmShown
		}
		se.post(self.url_login, data = login_data, headers = self.headers)

	def get_grade(self):
		self.login()
		url = self.url
		headers = self.headers
		r = se.get(url, headers = headers)
		s = BeautifulSoup(r.text, 'lxml')
		try:
			trs = s.find('tbody').find_all('tr')
		except:
			print('登录失败')
		print('学年学期'.ljust(16), '课程名称'.ljust(32), '学分'.ljust(20), '最终'.ljust(15), '绩点'.ljust(15))

		try:
			for tr in trs:
				try:
					tds = tr.find_all('td')
				except:
					print('登录失败')
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
			print('登陆失败')

grade = GetGrade()
grade.get_grade()
