# -*- coding:utf8 -*-
# function: file Split (by condition)

import pandas as pd

#fil_name
file_or = pd.read_csv('ETL1711W201.csv')
file_or.head()

x = 'file_or.xxx' #列名 直接用TAB键引出所需要的列名

#筛选条件1
a = file_or[x][0] #筛选条件1 假定在第一行
file1 = file_or[file_or[x] == a]
#删除原索引重建索引
file1 = file1.reset_index(drop=True) 

#找出另一个筛选条件的index值

#if 1 仅存在2个不同条件的情况下
min(file_or[file_or[x] != a].index)

-----多个条件直接看这里-----
#if 2 多个条件情况下（建议不多于10个）
file_or.drop_duplicates([x])

#筛选条件2
#b = file_or.x[-2:-1] #假定第二个条件在最后几行，获取对应的index
#c = file_or.x[index]
n = max(file_or.index) #已知index情况下直接输入index数
b = file_or[x][n] #筛选条件2，获得条件2的值
file2 = file_or[file_or[x] == b] #
#删除原索引重建索引
file2 = file2.reset_index(drop=True) 

#验证文件记录行数，看是否还需要进行拆分
len(file_or)
len(file1)
len(file2)

#如果文件记录行数仍然过大，进行index切片再写入
m = 800000
file3 = file2[0:m] #80W 条记录行数
file4 = file2[m:len(file2)] #剩余记录，注意80W不包括在file3里，需要在file4里记录，len(file2)超过最大index数但不影响计数

len(file3)
len(file4)

#先存为csv再手动另存为，写入excel很慢很慢
file1.to_csv('x.csv', index = False)
file2.to_csv('x.csv', index = False)
file3.to_csv('x.csv', index = False)
file4.to_csv('x.csv', index = False)


# 进阶方案
# 直接对特定列进行分组，进而将其按条件分为不同的csv文件
# 采用循环方式
