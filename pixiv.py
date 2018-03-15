from bs4 import BeautifulSoup
import requests
import os
import random
import time

se = requests.Session()

class PIXIV():
	def __init__(self, value, path):
		self.url = 'https://www.pixiv.net/ranking.php?mode=' + str(value)
		self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
		self.folder_path = path
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Referer' : 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
		}
		self.pixiv_id = 'your email'
		self.password = 'password'
		self.post_key = []
		self.return_to = 'http://www.pixiv.net/'
		self.ip_list = []

	def login(self):
		post_key_html = se.get(self.base_url, headers = self.headers).text
		post_key_soup = BeautifulSoup(post_key_html, 'lxml')
		self.post_key = post_key_soup.find('input')['value']
		login_data = {
			'pixiv_id' : self.pixiv_id,
			'password' : self.password,
			'return_to' : self.return_to,
			'post_key' : self.post_key
		}
		se.post(self.base_url, data = login_data, headers = self.headers)

	#使用IP代理
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

	def get_html(self, url, timeout, proxies = None, num_entries=5):
		if proxies == None:
			try:
				return se.get(url, headers = self.headers, timeout = timeout)
			except:
				if num_entries > 0:
					print('获取网页出错，5秒后重新获取倒数第', num_entries, '次')
					time.sleep(5)
					return self.get_html(url, timeout, num_entries = num_entries - 1)
				else:
					print('开始使用代理')
					time.sleep(5)
					ip_list = self.get_ip_list()
					random_ip = self.get_random_ip(ip_list)
					return self.get_html(url, proxies = random_ip)
		else:
			try:
				return se.get(url, headers = self.headers, proxies = proxies)
			except:
				if num_entries > 0:
					print('获取网页出错，5秒后重新获取倒数第', num_entries, '次')
					time.sleep(5)
					return self.get_html(url, timeout, num_entries = num_entries - 1)
				else:
					print('使用代理失败，取消使用代理')
					return self.get_html(url,timeout)

	def save_image(self, url, file_name):
		print('开始请求图片地址，过程会有点长...')
		img = self.get_html(url, 3)
		print('开始保存图片')
		f = open(file_name, 'ab')
		f.write(img.content)
		print(file_name, '图片保存成功!')
		f.close()

	def mkdir(self, path):   #这个函数创建文件夹
		path = path.strip()
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

	def start(self):
		print('start')
		self.login()
		time.sleep(3)
		r = se.get(self.url)
		soup = BeautifulSoup(r.text, 'lxml')
		pic_list = soup.find_all('section', class_ = 'ranking-item')

		self.mkdir(self.folder_path)  #创建文件夹
		print('开始切换文件夹')
		os.chdir(self.folder_path)    #切换路径至上面创建的文件夹

		file_names = self.get_files(self.folder_path)  #获取文件夹中的所有文件名，类型是list
		i = 5
		for pic in pic_list:
			link = pic.find('div', class_ = 'ranking-image-item').find('a')['href']
			r = se.get('https://www.pixiv.net' + str(link))
			#print(r.text)
			soup = BeautifulSoup(r.text, 'lxml')
			try:
				pic_url = soup.find('div', class_ = '_illust_modal _hidden ui-modal-close-box').find('img')['data-src']
				if pic_url[-3:] == 'png':
					name = soup.find('div', class_ ='_illust_modal _hidden ui-modal-close-box').find('img')['alt'] + '.png'
					name = name.replace("/", "")
					name = name.replace(":", "：")
				elif pic_url[-3:] == 'jpg':
					name = soup.find('div', class_='_illust_modal _hidden ui-modal-close-box').find('img')['alt'] + '.jpg'
					name = name.replace("/", "")
					name = name.replace(":", "：")
			except:
				continue
			name = name.encode('gbk', 'ignore').decode('gbk')
			print(pic_url, name)

			if name in file_names:
				print('图片已存在，不再重新下载')
			else:
				self.save_image(pic_url, name)
			i -= 1
			if i <= 0:
				break
			time.sleep(2)

value = input('请输入代号：日榜 = daily；周榜 = weekly；月榜 = monthly\n')
path = input('请输入文件夹路径\n')
pics = PIXIV(value, path)
pics.start()
