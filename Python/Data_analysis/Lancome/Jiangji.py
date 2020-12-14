# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: Jiangjitixing

from pandas import Series, DataFrame
import pandas as pd
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\LevelDown.csv', sep = '\t', encoding = 'utf-16')
data_revenue = pd.read_csv(path + file_current_name + '\LevelDownRevenue.csv', sep = '\t', encoding = 'utf-16')

data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Level Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

#取源数据之后需要的字段，并作去重处理
data_process_0 = pd.DataFrame(data, columns = ['Contact or Prospect ID', 'ROW_ID', 'Mobile Phone','Last Name', 'Level Name', 'Level_Number', 'Card End Date'])
data_process_0 = data_process_0.sort_values(by = ['Mobile Phone', 'Level_Number'], ascending = False)
data_process_0 = data_process_0.drop_duplicates('Mobile Phone')
data_process_0 = data_process_0.reset_index(drop = True)
#SUM值处理
data_com = pd.merge(data, data_revenue, how = 'left', on = ['Contact or Prospect ID', 'Mobile Phone', 'ROW_ID', 'Card Start Date'], suffixes = ('', '_right'))
data_com['U_Order Revenue'] = data_com['U_Order Revenue'].fillna(0)
data_com_groupby = data_com.groupby(data_com['Contact or Prospect ID'])['U_Order Revenue']
data_com_groupby_sum = data_com_groupby.sum().reset_index()
data_com_groupby_sum.rename(columns = {'U_Order Revenue': 'Total_Revenue'}, inplace = True)

data_process_1 = pd.merge(data_process_0, data_com_groupby_sum, how = 'left', on = 'Contact or Prospect ID', suffixes = ('', '_right'))
#data_process_1['id'] = random.sample(range(len(data_process_1.index)), len(data_process_1.index)) #为了字段顺序，放到各个部分建立id数
#data_process_1['Diff_Revenue']

filename = "Jiangji_Leveldown"
file_yinka0 = '-Yinka0'
file_yinka1 = '-Yinka1'
file_jinka = '-Jinka'
file_heika = '-Heika'
file_date = str(input('Enter File Date: '))
print ' '

# 黑金卡降级部分
data_heika = data_process_1[data_process_1['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458']
data_heika = data_heika[(data_heika['Total_Revenue'] > 0) & (data_heika['Total_Revenue'] <25000)]
data_heika['Diff_Revenue'] = map(lambda x: 25000 - x, data_heika['Total_Revenue'])
data_heika['id'] = random.sample(range(len(data_heika.index)), len(data_heika.index)) 
#删除索引重建
data_heika = data_heika.reset_index(drop = True)
con_flag_heika = data_heika['id']
con_flag_heika = sorted(con_flag_heika)
#Control组设置
if len(con_flag_heika) > (len(con_flag_heika) - len(con_flag_heika) / 10):
	data_heika['Control Group'] = map(lambda x: 'Control' if x>=con_flag_heika[len(con_flag_heika) - len(con_flag_heika) / 10 ] else 'Sending', data_heika['id'])
else:
	data_heika['Control Group'] = map(lambda x: 'Control' if x == max(data_heika['id']) else 'Sending', data_heika['id'])
#写文件
data_heika = pd.DataFrame(data_heika, columns = ['Contact or Prospect ID', 'ROW_ID', 'Mobile Phone','Last Name', 'Level Name', 'Card End Date', 'Total_Revenue', 'Diff_Revenue', 'id', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_heika.to_csv(path + file_current_name + '\\' + filename + file_heika + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_heika + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# 金卡降级部分
# 单笔满7000记录处理
data_com_groupby_jinka_max = data_com_groupby.max().reset_index()
data_com_groupby_jinka = data_com_groupby_jinka_max[data_com_groupby_jinka_max['U_Order Revenue'] >= 7000] #这是所有单笔7000记录，后续从里面剔除即可

data_jinka = data_process_1[data_process_1['Level Name'] == u'\u91d1\u5361\u4f1a\u5458']
data_jinka_1 = data_jinka[data_jinka['Total_Revenue'] >= 10000]
data_jinka = data_jinka[-data_jinka['Contact or Prospect ID'].isin(data_com_groupby_jinka['Contact or Prospect ID'])] # - - 注意这部分
data_jinka = data_jinka[-data_jinka['Mobile Phone'].isin(data_jinka_1['Mobile Phone'])]
data_jinka = data_jinka[data_jinka['Total_Revenue'] > 0]
data_jinka['Diff_Revenue'] = map(lambda x: 10000 - x, data_jinka['Total_Revenue'])
data_jinka['id'] = random.sample(range(len(data_jinka.index)), len(data_jinka.index)) 
#删除索引重建
data_jinka = data_jinka.reset_index(drop = True)
con_flag_jinka = data_jinka['id']
con_flag_jinka = sorted(con_flag_jinka)
#Control组设置
if len(con_flag_jinka) > (len(con_flag_jinka) - len(con_flag_jinka) / 10):
	data_jinka['Control Group'] = map(lambda x: 'Control' if x>=con_flag_jinka[len(con_flag_jinka) - len(con_flag_jinka) / 10 ] else 'Sending', data_jinka['id'])
else:
	data_jinka['Control Group'] = map(lambda x: 'Control' if x == max(data_jinka['id']) else 'Sending', data_jinka['id'])
#写文件
data_jinka = pd.DataFrame(data_jinka, columns = ['Contact or Prospect ID', 'ROW_ID', 'Mobile Phone','Last Name', 'Level Name', 'Card End Date', 'Total_Revenue', 'Diff_Revenue', 'id', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_jinka.to_csv(path + file_current_name + '\\' + filename + file_jinka + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_jinka + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# 银卡部分
#正负单处理
data_com['Flag'] = map(lambda x: 1 if x == 'Sale Order' else x, data_com['Order Type_I'])
data_com['Flag'] = map(lambda x: -1 if x == 'Return Order' else x, data_com['Flag'])
data_com['Flag'] = map(lambda x: 0 if pd.isnull(x) == True else x, data_com['Flag'])
data_com_groupby_yinka = data_com.groupby(data_com['Contact or Prospect ID'])['Flag']
data_com_groupby_yinka_sum = data_com_groupby_yinka.sum().reset_index()
data_process_2 = pd.merge(data_process_0, data_com_groupby_yinka_sum, how = 'left', on = 'Contact or Prospect ID', suffixes = ('', '_right'))
data_process_2 = data_process_2[data_process_2['Level Name'] == u'\u94f6\u5361\u4f1a\u5458']
data_process_2['id'] = random.sample(range(len(data_process_2.index)), len(data_process_2.index)) 

# 银卡1部分（只消费过1次）
data_yinka1 = data_process_2[data_process_2['Flag'] == 1]
#删除索引重建
data_yinka1 = data_yinka1.reset_index(drop = True)
con_flag_yinka1 = data_yinka1['id']
con_flag_yinka1 = sorted(con_flag_yinka1)
#Control组设置
if len(con_flag_yinka1) > (len(con_flag_yinka1) - len(con_flag_yinka1) / 10):
	data_yinka1['Control Group'] = map(lambda x: 'Control' if x>=con_flag_yinka1[len(con_flag_yinka1) - len(con_flag_yinka1) / 10 ] else 'Sending', data_yinka1['id'])
else:
	data_yinka1['Control Group'] = map(lambda x: 'Control' if x == max(data_yinka1['id']) else 'Sending', data_yinka1['id'])
#写文件
data_yinka1 = pd.DataFrame(data_yinka1, columns = ['Contact or Prospect ID', 'ROW_ID', 'Mobile Phone','Last Name', 'Level Name', 'Card End Date', 'id', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_yinka1.to_csv(path + file_current_name + '\\' + filename + file_yinka1 + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_yinka1 + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# 银卡0部分（未消费过）
data_yinka0 = data_process_2[data_process_2['Flag'] <= 0]
data_yinka_cuoci = data_process_2[data_process_2['Flag'] >= 1] #其实不需要
data_yinka0 = data_yinka0[-data_yinka0['Mobile Phone'].isin(data_yinka_cuoci['Mobile Phone'])]
#删除索引重建
data_yinka0 = data_yinka0.reset_index(drop = True)
con_flag_yinka0 = data_yinka0['id']
con_flag_yinka0 = sorted(con_flag_yinka0)
#Control组设置
if len(con_flag_yinka0) > (len(con_flag_yinka0) - len(con_flag_yinka0) / 10):
	data_yinka0['Control Group'] = map(lambda x: 'Control' if x>=con_flag_yinka0[len(con_flag_yinka0) - len(con_flag_yinka0) / 10 ] else 'Sending', data_yinka0['id'])
else:
	data_yinka0['Control Group'] = map(lambda x: 'Control' if x == max(data_yinka0['id']) else 'Sending', data_yinka0['id'])
#写文件
data_yinka0 = pd.DataFrame(data_yinka0, columns = ['Contact or Prospect ID', 'ROW_ID', 'Mobile Phone','Last Name', 'Level Name', 'Card End Date', 'id', 'Control Group'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_yinka0.to_csv(path + file_current_name + '\\' + filename + file_yinka0 + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_yinka0 + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '