#-*- coding: utf-8 -*-

# 背景：在用SQL处理CSV文件时，经常会遇到编码方式不同的情况，因此写了本程序，用于快速查看指定文件编码方式
# 功能：快速查看指定文件的编码方式

import chardet
import os

# abspath = "E:\Programming\\tools" # 指定文件查找路径
abspath = os.getcwd() # os.getcwd() 获取当前工作路径

def printchar():
	f = open(filename, 'r')
	data = f.read()
	print "Path:", filepath # 输出当前文件绝对路径
	print "File %s:" % n, filerename # 输出文件名，对文件进行编号
	print "Property:", chardet.detect(data) # 输出文件编码方式
	print "" # 换行

n = 1 # 文件编号

for root, dirs, files in os.walk(abspath): # os.walk() 遍历目录, os.getcwd() 获取当前工作路径（由此可得可以修改指定目录）
        for f in files:
            if f.lower().endswith('.csv'): #查找需要查看编码方式的 .csv 文件
                filename = os.path.join(root, f) # 获取文件绝对路径，用于读取文件内容进行判断
                # filepath = os.path.basename(root) # 获取文件名或文件夹名
                filepath = os.path.abspath(root) # 获取查看的文件所在绝对目录
                filerename = os.path.basename(f) # 获取文件名
                printchar()
                n = n + 1 # 文件计数
				



