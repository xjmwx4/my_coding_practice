# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: LifecycleM3

from pandas import Series, DataFrame
import pandas as pd
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\LifecycleM3.csv', sep = '\t', encoding = 'utf-16')
data_revenue = pd.read_csv(path + file_current_name + '\LifecycleM3Revenue.csv', sep = '\t', encoding = 'utf-16')

data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Level Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

data_com = pd.merge(data, data_revenue, how = 'left', on = ['Mobile Phone', 'Card Start Date'], suffixes = ('', '_right'))
data_com['Order Revenue'] = data_com['Order Revenue'].fillna(0)
data_process_1 = pd.DataFrame(data_com, columns = ['Mobile Phone','Last Name', 'Points', 'Level Name', 'Level_Number', 'Card End Date', 'Amount of Active Card', 'Order Revenue'])
data_groupby = data_process_1.groupby([data_process_1['Mobile Phone'],data_process_1['Level_Number']])['Order Revenue']
data_groupby_sum = data_groupby.sum().reset_index()
data_process_0 = pd.DataFrame(data_com, columns = ['Mobile Phone','Last Name', 'Points', 'Level Name', 'Level_Number', 'Card End Date', 'Amount of Active Card'])
data_process_0 = data_process_0.sort_values(by = ['Mobile Phone', 'Level_Number', 'Points'], ascending = False)
data_process_0 = data_process_0.drop_duplicates(['Mobile Phone'])
data_process_0 = data_process_0.reset_index(drop = True)
data_end = pd.merge(data_process_0, data_groupby_sum, how = 'left', on = ['Mobile Phone', 'Level_Number'])
data_end.rename(columns={'Order Revenue':'Total_Revenue'}, inplace = True)

data_end['id'] = random.sample(range(len(data_end.index)), len(data_end.index))

filename = "LifecycleM3"
file_Puka = '-Puka'
file_NotJinka = '-NotJinka'
file_NotHeika = '-NotHeika'
file_else = '-else'
file_date = str(input('Enter File Date: '))
print ' '

#Lifecycle M3 普卡部分
data_Puka = data_end[data_end['Level Name'] == u'\u666e\u901a\u4f1a\u5458']
#删除索引重建
data_Puka = data_Puka.reset_index(drop=True) 
con_flag_Puka = data_Puka['id']
con_flag_Puka = sorted(con_flag_Puka)
#Control组设置
data_Puka['Control Group'] = map(lambda x: 'Control' if x>=con_flag_Puka[len(con_flag_Puka) - len(con_flag_Puka) / 10 ] else 'Sending', data_Puka['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_Puka.to_csv(path + file_current_name + '\\' + filename + file_Puka + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_Puka + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

#Lifecycle M3 7500-1W 非金卡部分
data_NotJinka_process = data_end[data_end['Level Name'] != u'\u91d1\u5361\u4f1a\u5458']
#data_NotJinka_process = data_end[(data_end['Level Name'] != u'\u91d1\u5361\u4f1a\u5458') & (data_end['Level Name'] != u'\u9ed1\u91d1\u5361\u4f1a\u5458')]
data_NotJinka_process = data_NotJinka_process[-data_NotJinka_process['Mobile Phone'].isin(data_Puka['Mobile Phone'])]
data_NotJinka_process = data_NotJinka_process[(data_NotJinka_process['Total_Revenue'] >= 7500) & (data_NotJinka_process['Total_Revenue'] < 10000)]
data_NotJinka_process['Diff_Revenue'] = map(lambda x: 10000 - x , data_NotJinka_process['Total_Revenue'])
#删除索引重建
data_NotJinka_process = data_NotJinka_process.reset_index(drop=True) 
con_flag_NotJinka = data_NotJinka_process['id']
con_flag_NotJinka = sorted(con_flag_NotJinka)
#Control组设置
if len(con_flag_NotJinka) > (len(con_flag_NotJinka) - len(con_flag_NotJinka) / 10):
	data_NotJinka_process['Control Group'] = map(lambda x: 'Control' if x>=con_flag_NotJinka[len(con_flag_NotJinka) - len(con_flag_NotJinka) / 10 ] else 'Sending', data_NotJinka_process['id'])
else:
	data_NotJinka_process['Control Group'] = map(lambda x: 'Control' if x == max(data_NotJinka_process['id']) else 'Sending', data_NotJinka_process['id'])
#写文件
data_NotJinka = pd.DataFrame(data_NotJinka_process, columns = ['Mobile Phone','Last Name', 'Points', 'Level Name', 'Card End Date', 'Amount of Active Card', 'Diff_Revenue', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_NotJinka.to_csv(path + file_current_name + '\\' + filename + file_NotJinka + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_NotJinka + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

#Lifecycle M3 2W-2W5 非黑卡部分
data_NotHeika_process = data_end[data_end['Level Name'] != u'\u9ed1\u91d1\u5361\u4f1a\u5458']
data_NotHeika_process = data_NotHeika_process[-data_NotHeika_process['Mobile Phone'].isin(data_Puka['Mobile Phone'])]
data_NotHeika_process = data_NotHeika_process[-data_NotHeika_process['Mobile Phone'].isin(data_NotJinka['Mobile Phone'])]
data_NotHeika_process = data_NotHeika_process[(data_NotHeika_process['Total_Revenue'] >= 20000) & (data_NotHeika_process['Total_Revenue'] < 25000)]
data_NotHeika_process['Diff_Revenue'] = map(lambda x: 25000 - x , data_NotHeika_process['Total_Revenue'])
#删除索引重建
data_NotHeika_process = data_NotHeika_process.reset_index(drop=True) 
con_flag_NotHeika = data_NotHeika_process['id']
con_flag_NotHeika = sorted(con_flag_NotHeika)
#Control组设置
if len(con_flag_NotHeika) > (len(con_flag_NotHeika) - len(con_flag_NotHeika) / 10):
	data_NotHeika_process['Control Group'] = map(lambda x: 'Control' if x>=con_flag_NotHeika[len(con_flag_NotHeika) - len(con_flag_NotHeika) / 10 ] else 'Sending', data_NotHeika_process['id'])
else:
	data_NotHeika_process['Control Group'] = map(lambda x: 'Control' if x == max(data_NotHeika_process['id']) else 'Sending', data_NotHeika_process['id'])
#写文件
data_NotHeika = pd.DataFrame(data_NotHeika_process, columns = ['Mobile Phone','Last Name', 'Points', 'Level Name', 'Card End Date', 'Amount of Active Card', 'Diff_Revenue', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_NotHeika.to_csv(path + file_current_name + '\\' + filename + file_NotHeika + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_NotHeika + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

#Lifecycle M3 除去以上三类
data_else_process = data_end[-data_end['Mobile Phone'].isin(data_Puka['Mobile Phone'])]
data_else_process = data_else_process[-data_else_process['Mobile Phone'].isin(data_NotJinka['Mobile Phone'])]
data_else_process = data_else_process[-data_else_process['Mobile Phone'].isin(data_NotHeika['Mobile Phone'])]
#删除索引重建
data_else_process = data_else_process.reset_index(drop=True) 
con_flag_else = data_else_process['id']
con_flag_else = sorted(con_flag_else)
#Control组设置
if len(con_flag_else) > (len(con_flag_else) - len(con_flag_else) / 10):
	data_else_process['Control Group'] = map(lambda x: 'Control' if x>=con_flag_else[len(con_flag_else) - len(con_flag_else) / 10 ] else 'Sending', data_else_process['id'])
else:
	data_else_process['Control Group'] = map(lambda x: 'Control' if x == max(data_else_process['id']) else 'Sending', data_else_process['id'])
#写文件
data_else = pd.DataFrame(data_else_process, columns = ['Mobile Phone','Last Name', 'Points', 'Level Name', 'Card End Date', 'Amount of Active Card', 'id', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_else.to_csv(path + file_current_name + '\\' + filename + file_else + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_else + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '