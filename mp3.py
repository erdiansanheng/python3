from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
import random

class MP3():
	def __init__(self, list_id, path):
		self.base_url = 'http://www.xiami.com'
		self.list_url = 'http://www.xiami.com/collect/' + str(list_id)
		self.folder_path = path
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
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

	def save_mp3(self, url, file_name):
		print('开始请求mp3地址，过程会有点长...')
		mp3 = self.get_html(url)
		print('开始保存mp3')
		f = open(file_name, 'ab')
		f.write(mp3.content)
		print(file_name, '  mp3保存成功!\n')
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

	def get_id(self):
		r = requests.get(self.list_url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		all_li = soup.find('div', class_ = 'quote_song_list').find_all('li')
		song_ids = []
		for li in all_li:
			temp = li['id']
			id = temp[6:]
			song_ids.append(id)
		return song_ids

	def get_name(self):
		r = requests.get(self.list_url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		all_url = soup.find('div', class_ = 'quote_song_list').find_all('span', class_ = 'song_name')
		names = []
		for url in all_url:
			title = url.find_all('a')
			name = title[0]['title']
			name = name.replace("/", "")
			name = name.replace(":", "：")
			names.append(name)
		return names

	def get_url(self, song_id):
		xml_url = 'http://www.xiami.com/song/playlist/id/' + str(song_id) + '/object_name/default/object_id/0'
		r = requests.get(xml_url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		l = soup.find('location')
		if l == None:
			print('该歌曲不能下载')
			return None
		l = l.string
		rows = int(l[0])
		new_str = l[1:]
		strlen = len(new_str)
		cols = strlen // rows
		right_rows = strlen % rows
		mp3_url = ''
		for i in range(strlen):
			x = i % rows
			y = i / rows
			p = 0
			if x <= right_rows:
				p = x * (cols + 1) + y
			else:
				p = right_rows * (cols + 1) + (x - right_rows) * cols + y
			mp3_url += new_str[int(p)]
		mp3_url = urllib.parse.unquote(mp3_url).replace("^", "0")
		return mp3_url

	def get_list_name(self):
		r = requests.get(self.list_url, headers = self.headers)
		soup = BeautifulSoup(r.text, 'lxml')
		name = soup.find('head').find('title').string
		list_name = '\\' + name
		return list_name

	def start(self):
		print('start')
		names = self.get_name()
		ids = self.get_id()

		self.folder_path += self.get_list_name()
		self.mkdir(self.folder_path)  #创建文件夹
		print('开始切换文件夹')
		os.chdir(self.folder_path)    #切换路径至上面创建的文件夹
		file_names = self.get_files(self.folder_path)  #获取文件夹中的所有文件名，类型是list

		for i in range(len(names)):
			file_name = names[i] + '.mp3'
			song_id = ids[i]
			mp3_url = self.get_url(song_id)
			if file_name in file_names:
				print('mp3已存在，不再重新下载')
			else:
				if mp3_url == None:
					print('继续下载下一首歌曲')
				else:
					self.save_mp3(mp3_url, file_name)

list_id = input('请输入歌单id')
path = input('请输入文件夹路径')
mp3 = MP3(list_id, path)
mp3.start()