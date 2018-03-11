#!usr/bin/python

import random

number = random.choice(range(100))
guess = -1

while guess != number:
	guess = int(input("请输入你猜的数:"))

	if guess == number:
		print ("你猜对了！")
	elif guess < number:
		print ("你猜的数小了...")
	else:
		print ("你猜的数大了...")