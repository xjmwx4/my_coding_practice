# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: BirthdayMonthly-Offline-18th

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data_27 = pd.read_csv(path + file_current_name + '\BirthdayMonthly.csv', sep = '\t', encoding = 'utf-16')
#data_18 = pd.read_csv(path + file_current_name + '\BirthdayMonthly_18th.csv', sep = '\t', encoding = 'utf-16')
data_18 = pd.read_csv(path + file_current_name + '\BirthdayMonthly_18th.csv', encoding = 'utf-8-sig')

#会员等级处理 新增 Level_Number 字段
data_18['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data_18['Level Name']) 								#GC
data_18['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data_18['Level_Number']) 		#普通会员
data_18['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data_18['Level_Number']) 		#银卡会员
data_18['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data_18['Level_Number']) 		#金卡会员
data_18['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data_18['Level_Number']) 	#黑金卡会员

#会员等级处理 新增 Level_Number 字段
data_27['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data_27['Level Name']) 								#GC
data_27['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data_27['Level_Number']) 		#普通会员
data_27['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data_27['Level_Number']) 		#银卡会员
data_27['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data_27['Level_Number']) 		#金卡会员
data_27['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data_27['Level_Number']) 	#黑金卡会员

data_18_drop = data_18.sort_values(by = ['Mobile Phone', 'Level_Number', 'Contact or Prospect ID'], ascending = False)
data_18_drop = data_18_drop.drop_duplicates(['Mobile Phone'])
data_18_drop = data_18_drop.reset_index(drop = True)

data_27_drop = data_27.sort_values(by = ['Mobile Phone', 'Level_Number', 'Contact or Prospect ID'], ascending = False)
data_27_drop = data_27_drop.drop_duplicates(['Mobile Phone'])
data_27_drop = data_27_drop.reset_index(drop = True)

data_27_com = pd.merge(data_18_drop, data_27_drop, how = 'left', on = ['Contact or Prospect ID', 'Mobile Phone'], suffixes = ('', '_right'))
data_27_com['Max_Level_Name'] = map(lambda x,y,p,q: p if x > y else q, data_27_com['Level_Number'], data_27_com['Level_Number_right'], data_27_com['Level_Number'], data_27_com['Level_Number_right']) 
data_27_com_0 = pd.DataFrame(data_27_com, columns = ['Contact or Prospect ID', 'ROW_ID', 'Pure Control Flag', 'Pure Control Real Remain Date', 'Mobile Phone', 'SMS Quality', 'SMS Permission', 'Last Name', 'Birthday', 'Counter Name New', 'Local Counter Name New', 'Amount of Active Card', 'Max_Level_Name', 'Points', 'Last Sale Order Date', 'Last Order Amount'])

#PCG人群标记，剔除TMALL EC人群，取手机号为11位
data_27_com_0['PCG_Flag'] = map(lambda x,y: 'Y' if (pd.isnull(x) == False and pd.isnull(y) == True) else 'N', data_27_com_0['Pure Control Flag'], data_27_com_0['Pure Control Real Remain Date']) 
data_27_com_0 = data_27_com_0[-data_27_com_0['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986', 'ChinaLancome6P0'])]
data_27_com_0['Phone_Flag'] = map(lambda x: True if len(str(x)) == 11 else False, data_27_com_0['Mobile Phone'])
data_27_com_0 = data_27_com_0[data_27_com_0['Phone_Flag'] == True]

filename_quanliang = u'\u751f\u65e5\u793c\u7269\u9886\u53d6' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708'
filename_yinkayishang = u'\u751f\u65e5\u793c\u7269\u9886\u53d6' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708' + u'\u002d\u94f6\u5361\u53ca\u4ee5\u4e0a'
file_date = str(input('Enter File Date (MMDD): '))
print ' '

data_quanliang = data_27_com_0.iloc[:]
data_quanliang = data_quanliang.reset_index(drop = True)
data_quanliang.to_csv(path + file_current_name + '\\' + filename_quanliang + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename_quanliang + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

data_yinkayishang = data_27_com_0[(data_27_com_0['Max_Level_Name'] == u'\u94f6\u5361\u4f1a\u5458') | (data_27_com_0['Max_Level_Name'] == u'\u91d1\u5361\u4f1a\u5458') | (data_27_com_0['Max_Level_Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458')]
data_yinkayishang = data_yinkayishang.reset_index(drop = True)
data_yinkayishang.to_csv(path + file_current_name + '\\' + filename_yinkayishang + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename_yinkayishang + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '