# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: BirthdayMonthly-Offline-18th

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
#path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
path = 'C:\Users\Administrator\python1208\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\BirthdayMonthly_18th.csv', sep = '\t', encoding = 'utf-16')
data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Level Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

data['Phone_Flag'] = map(lambda x: len(x), data['Mobile Phone'])


data = data.sort_values(by = ['Mobile Phone', 'Level_Number', 'Contact or Prospect ID'], ascending = False)
data = data.drop_duplicates(['Mobile Phone'])
data['Phone_Flag'] = map(lambda x: True if len(str(x)) == 11 else False, data['Mobile Phone'])
data = data[data['Phone_Flag'] == True]
data = data.reset_index(drop = True)

filename = u'\u751f\u65e5\u793c\u7269\u9886\u53d6\u0031\u0038\u0074\u0068' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708'
filename_yinkayishang = u'\u751f\u65e5\u793c\u7269\u9886\u53d6\u0031\u0038\u0074\u0068' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708' + u'\u002d\u94f6\u5361\u53ca\u4ee5\u4e0a'
file_date = str(input('Enter File Date (MMDD): '))
print ' '

data.to_csv(path + file_current_name + '\\' + filename + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

data_yinkayishang = data[(data['Level Name'] == u'\u94f6\u5361\u4f1a\u5458') | (data['Level Name'] == u'\u91d1\u5361\u4f1a\u5458') | (data['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458')]
data_yinkayishang = data_yinkayishang.reset_index(drop = True)
data_yinkayishang.to_csv(path + file_current_name + '\\' + filename_yinkayishang + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename_yinkayishang + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '