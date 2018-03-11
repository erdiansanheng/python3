# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os

class SL():
	def __init__(self, songList_id, path):
		self.init_url = 'http://music.163.com/#/playlist?id=' + str(songList_id)
		self.folder_path = str(path)

	def saveSongs(self, url, file_name):
		print('开始请求歌曲地址...')
		song = requests(url)
		print('开始保存歌曲')
		f = open(file_name, 'ab')
		f.write(song.content)
		print(file_name, '歌曲保存成功')
		f.close()

	def request(self, url):
		r = requests.get(url)
		return r

	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			print('创建名字叫做', path, '的文件夹')
			os.makedirs(path)
			print('创建成功')
			return True
		else:
			print(path, '文件夹已经存在了')
			return False

	def get_files(self, path):
		song_names = os.listdir(path)
		return song_names

	def start(self):
		print('start')
		driver = webdriver.PhantomJS()
		driver.get(self.init_url)
		driver.switch_to.frame('g_iframe')
		html = driver.page_source

		self.mkdir(self.folder_path)
		print('开始切换文件夹')
		os.chdir(self.folder_path)

		file_names = self.get_files(self.folder_path)

		all_tr = BeautifulSoup(html, 'lxml').find('table', class_ = 'm-table').find('tbody').find_all('tr')

		for tr in all_tr:
			song = tr.find('a')['href']
			song_name = tr.find('b').get_text()
			song_url = 'http://music.163.com/#' + str(song)

			song_name = song_name.replace("/", "")
			song_name = song_name.replace(":", ",")
			songFile_name = song_name + '.mp3'
			print(song_url, song_name)

			if songFile_name in file_names:
				print('歌曲已存在')
			else:
				self.saveSongs(song_url, songFile_name)

songs_id = input('请输入歌单id')
path = input('请输入要创建的歌单路径')
songList = SL(songs_id, path)
songList.start()
