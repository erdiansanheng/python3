from bs4 import BeautifulSoup
import requests
import os


url = 'https://lh3.googleusercontent.com/Sd7arudcIsZWe9rUNYIAryKxtMiWPpZUdFlOMtEcnR3DyTQrPOMfGXFjEVBf-pNO4LB8-fblGBiqdkCg-8JwUf8=h600-l90'
header = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Referer' : 'https://lh3.googleusercontent.com/Sd7arudcIsZWe9rUNYIAryKxtMiWPpZUdFlOMtEcnR3DyTQrPOMfGXFjEVBf-pNO4LB8-fblGBiqdkCg-8JwUf8=h600-l90'
}
r = requests.get(url, headers = header)

f = open('G:\\python小程序\\python3\\1.png', 'ab')
f.write(r.content)
print('图片保存成功')
f.close()