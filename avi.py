from bs4 import BeautifulSoup
import requests
import os
import random

class AVI():
	def __init__(self, path, page):
		self.base_url = 'https://www.po3po.com'
		self.url = 'https://www.po3po.com/photo/pic2/page/' + str(page)
		self.folder_path = path
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Referer' : 'https://www.po3po.com/'
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
		all_li = soup.find('ul', class_ = 'text-list').find_all('li')
		urls = []
		for li in all_li:
			href = li.find('a')['href']
			url = 'https://www.po3po.com' + str(href)
			urls.append(url)
		return urls

	def get_pic_url(self, url):
		r = requests.get(url, headers = self.pic_headers)
		#print(r.text)
		soup = BeautifulSoup(r.text, 'lxml')
		imgs = soup.find('div', class_ = 'text-content').find_all('img')
		urls = []
		for img in imgs:
			url = self.base_url + str(img['src'])
			urls.append(url)
		return urls

	def get_folder_name(self):
		r = requests.get(self.url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		all_li = soup.find('ul', class_ = 'text-list').find_all('li')
		names = []
		for li in all_li:
			name = li.find('a')['title']
			name = name.replace(u'\xa0', u' ')
			names.append(name)
		return names

	def start(self):
		print('start')

		self.mkdir(self.folder_path)  #创建文件夹
		names = self.get_folder_name()
		for name in names:
			self.mkdir(self.folder_path + '\\' + name)

		urls = self.get_pics_urls()
		for i in range(len(urls)):
			print(urls[i])
			pic_urls = self.get_pic_url(urls[i])
			os.chdir(self.folder_path + '\\' + names[i])
			print('开始切换文件夹')
			file_names = self.get_files(self.folder_path + '\\' + names[i])
			j = 1
			for pic_url in pic_urls:
				name = str(j) + '.jpg'
				j += 1
				print(pic_url, name)
				if name in file_names:
					print('图片已存在，不再重新下载')
				else:
					self.save_image(pic_url, name)

page = input('输入页码')
page = str(page)
path = input('输入文件夹路径')
pics = AVI(path, page)
pics.start()
