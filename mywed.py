from bs4 import BeautifulSoup
import requests
import os
import random

class MyWed():
	def __init__(self, path, page, section):
		self.base_url = 'https://mywed.com'
		self.url = 'https://mywed.com/zh/story/' + str(section) + str(page)
		self.folder_path = path
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Referer' : 'https://mywed.com'
		}
		self.pic_headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Referer': self.url
		}

	def get_ip_list(self):
		web_data = requests.get('http://www.xicidaili.com/nn/', headers = self.headers)
		soup = BeautifulSoup(web_data.text, 'lxml')
		ips = soup.find_all('tr')
		ip_list = []
		for i in range(1, len(ips)):
			ip_info = ips[i]
			tds = ip_info.find_all('td')
			ip_list.append(tds[1].text + ':' + tds[2].text)
		return ip_list

	def get_random_ip(self, ip_list):
		proxy_list = []
		for ip in ip_list:
			proxy_list.append('http://' + ip)
		proxy_ip = random.choice(proxy_list)
		print('当前使用代理', proxy_ip)
		proxies = {'http' : proxy_ip}
		return proxies

	def get_html(self, url, proxies = None):
		if proxies == None:
			try:
				return requests.get(url, headers = self.headers)
			except:
				print('开始使用代理')
				ip_list = self.get_ip_list()
				random_ip = self.get_random_ip(ip_list)
				return self.get_html(url, proxies = random_ip)
		else:
			try:
				return requests.get(url, headers = self.headers, proxies = proxies)
			except:
				print('正在更换代理')
				ip_list = self.get_ip_list()
				random_ip = self.get_random_ip(ip_list)
				return self.get_html(url, proxies = random_ip)

	def save_image(self, url, file_name):
		print('开始请求图片地址，过程会有点长...')
		img = self.get_html(url)
		print('开始保存图片')
		f = open(file_name, 'ab')
		f.write(img.content)
		print(file_name, '图片保存成功!')
		f.close()

	def mkdir(self, path):   #这个函数创建文件夹
		path = path.strip().replace(u'\xa0', u' ')
		path = path.strip().replace(u'\xf1', u' ')
		path = path.strip().replace(u'\u010d', u' ')
		isExists = os.path.exists(path)
		if not isExists:
			print('创建名字叫做', path, '的文件夹')
			os.makedirs(path)
			print('创建成功!')
			return True
		else:
			print(path, '文件夹已经存在了')
			return False

	def get_files(self, path):  #获取文件夹中的文件名称列表
		pic_names = os.listdir(path)
		return pic_names

	def get_pics_urls(self):
		r = requests.get(self.url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		all_div = soup.find_all('div', class_ = 'photo-story-view')
		urls = []
		for div in all_div:
			a = div.find('a', class_ = 'main-photo-toggle-block')
			href = a['href']
			url = self.base_url + str(href)
			urls.append(url)
		return urls

	def get_pic_url(self, url):
		r = requests.get(url, headers = self.pic_headers)
		#print(r.text)
		soup = BeautifulSoup(r.text, 'lxml')
		imgs = soup.find('div', class_ = 'story-view-detail-photogrid clearfix ').find_all('img')
		urls = []
		for img in imgs:
			url = str(img['src'])
			url = url.replace('=h400-l90', '=h2000-l90') #修改‘2000’可以改变图片质量，数值越高质量越好
			urls.append(url)
		return urls

	def get_folder_name(self):
		r = requests.get(self.url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		all_div = soup.find_all('div', class_ = 'photo-story-view')
		names = []
		for div in all_div:
			a = div.find('a', class_ = 'main-photo-toggle-block')
			#print(str(a).replace(u'\xf1', u' '))
			ns = a.find_all('span')
			name = ns[0].string.strip() + '-' + ns[1].string.strip()
			if ns[2].string is not None:
				name = name + '-' + ns[2].string.strip()
			name = name.replace(u'\xa0', u' ')
			name = name.replace(u'\xf1', u' ')
			name = name.replace(u'\u010d', u' ')
			name = name.replace(':', ' ')
			name = name.replace('|', ' ')
			name = name.replace('*', ' ')
			name = name.replace('?', ' ')
			name = name.replace('<', ' ')
			name = name.replace('>', ' ')
			name = name.replace('/', ' ')
			names.append(name)
		return names

	def start(self):
		print('start')

		self.mkdir(self.folder_path)  #创建文件夹
		names = self.get_folder_name()
		for name in names:
			self.mkdir(self.folder_path + '\\' + str(name))

		urls = self.get_pics_urls()
		for i in range(len(urls)):
			print(urls[i])
			pic_urls = self.get_pic_url(urls[i])
			os.chdir(self.folder_path + '\\' + names[i])
			print('开始切换文件夹')
			file_names = self.get_files(self.folder_path + '\\' + names[i])
			j = 1
			for pic_url in pic_urls:
				name = str(j) + '.png'
				j += 1
				print(pic_url, name)
				if name in file_names:
					print('图片已存在，不再重新下载')
				else:
					self.save_image(pic_url, name)


print('1.本周最佳  2.年度最佳  3.编辑精选')
sec = input('输入对应序号，回车确认：')
section = ''
if int(sec) == 1:
	section = ''
elif int(sec) == 2:
	section = 'day/'
elif int(sec) == 3:
	section = 'editors/'

num = input('想抓取第几页图集：')
path = input('输入文件夹路径:')


page = 'p' + str(num)
pics = MyWed(path, page, section)
pics.start()
