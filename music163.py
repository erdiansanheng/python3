# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os

class AlbumCover():
	def __init__(self, album_id, path):
		self.init_url = 'http://music.163.com/#/artist/album?id=' + str(album_id) + '&limit=120&offset=0'
		self.folder_path = str(path)

	def save_image(self, url, file_name):
		print('开始请求图片地址，过程会有点长...')
		img = self.request(url)
		print('开始保存图片')
		f = open(file_name, 'ab')
		f.write(img.content)
		print(file_name, '图片保存成功!')
		f.close()

	def request(self, url):
		r = requests.get(url)
		return r

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

	def spider(self):
		print('start')
		driver = webdriver.PhantomJS()
		driver.get(self.init_url)
		driver.switch_to.frame('g_iframe')
		html = driver.page_source

		self.mkdir(self.folder_path)  #创建文件夹
		print('开始切换文件夹')
		os.chdir(self.folder_path)    #切换路径至上面创建的文件夹

		file_names = self.get_files(self.folder_path)  #获取文件夹中的所有文件名，类型是list

		all_li = BeautifulSoup(html, 'lxml').find(id = 'm-song-module').find_all('li')

		for li in all_li:
			album_img = li.find('img')['src']
			album_name = li.find('p', class_ = 'dec')['title']
			album_date = li.find('span', class_ = 's-fc3').get_text()
			end_pos = album_img.index('?')
			album_img_url = album_img[:end_pos]

			album_name = album_name.replace("/", "")
			album_name = album_name.replace(":", ",")
			photo_name = album_date + ' - ' + album_name + '.jpg'
			print(album_img_url, photo_name)

			if photo_name in file_names:
				print('图片已存在，不再重新下载')
			else:
				self.save_image(album_img_url, photo_name)

album_id = input("请输入网易云音乐专辑id:")
path = input("请输入要创建的专辑封面路径:")
album_cover = AlbumCover(album_id, path)
album_cover.spider()