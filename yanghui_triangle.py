#!usr/bin/python

def triangles():
	L = [1]
	while True:
		yield L
		L = [1] + [L[x] + L[x + 1] for x in range(len(L) - 1)] + [1]

n = 0
m = int(input("请输入杨辉三角阶数："))
for t in triangles():
	print(t)
	n = n + 1
	if n == m:
		break;