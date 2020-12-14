# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: OfflineD3 & OnlineD3

from pandas import Series, DataFrame
import numpy as np
import pandas as pd
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
#path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
path = 'C:\Users\Administrator\python1208\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\OfflineOnlineD3.csv', sep = '\t', encoding = 'utf-16')

data = data[data['Order Revenue'] != 0]
data['Counter Employee Full Name'] = map(lambda x: x.replace(', -', '') if pd.isnull(x) == False else x, data['Counter Employee Full Name']) # BA Name部分字符串处理


data_offline = data[-data['Counter Name'].isin(['ChinaLancome976', 'ChinaLancome986'])]
data_TMALL = data[data['Counter Name'].isin(['ChinaLancome976'])]
data_EC = data[data['Counter Name'].isin(['ChinaLancome986'])]

filename = "OfflineOnlineDay3"
#filename_online = 'OnlineDay3'
file_TMALL = 'TMALL'
file_EC = 'EC'
file_date = str(input('Enter File Date (MMDD): '))
flag_month = str(input('Enter Month for manyidu (MM): '))
SendingTime = input('Enter SendingTime Date(str'' yyyyMMDD yinhao): ')
SendingTime2 = pd.to_datetime(SendingTime).strftime('%Y/%m/%d')
print ' '

#正负单处理，取正单记录
data_offline_grby = data_offline.iloc[:]
data_offline_grby = data_offline_grby.reset_index(drop = True)
data_offline_grby['Flag'] = map(lambda x: 1 if x == 'Sale Order' else -1, data_offline_grby['Order Type_I'])
data_offline_grby_groupby = data_offline_grby.groupby(data_offline_grby['Contact or Prospect ID'])['Flag']
data_offline_grby_sum = data_offline_grby_groupby.sum().reset_index() #groupby重塑
data_offline_grby_sum = data_offline_grby_sum[data_offline_grby_sum['Flag']>0] #取正单
data_offline = data_offline_grby[data_offline_grby['Contact or Prospect ID'].isin(data_offline_grby_sum['Contact or Prospect ID'])] #offline的所有消费记录
data_offline = data_offline[(data_offline['Order Revenue'] >= 180) & (data_offline['Order Revenue'] < 100000)] # 取180-99999 消费记录的人 此处只有 Sale Order的记录了
data_offline = data_offline.sort_values(by = ['Mobile Phone', 'Order Date', 'Order Id'], ascending = False)
data_offline = data_offline.drop_duplicates(['Mobile Phone', 'Order Date',]) # 按Mobile Phone, Order Date来去重，取最大一笔订单Order Id(上面一步排序)
data_offline['id'] = random.sample(range(len(data_offline.index)), len(data_offline.index)) 
data_offline['Rank_id'] = data_offline.groupby(data_offline['Mobile Phone'])['Order Date'].rank() # by Mobile Phone by Order Date 组内排序

for x in range(1, 1+int(max(data_offline['Rank_id']))): #构造循环
	data_process = data_offline[data_offline['Rank_id'] == np.float64(x)] #取rank = 1,2,3...
	data_process = data_process.reset_index(drop = True)
	con_flag_process = data_process['id']
	con_flag_process = sorted(con_flag_process)
	#Control组设置
	if len(con_flag_process) > (len(con_flag_process) - len(con_flag_process) / 10): # len >= 10时，进行Control组比例设置
		data_process['Control Group'] = map(lambda x: 'Control' if x>=con_flag_process[len(con_flag_process) - len(con_flag_process) / 10 ] else 'Sending', data_process['id'])
	else: # len < 10时，取id最大的一个值作为control组
		data_process['Control Group'] = map(lambda x: 'Control' if x == max(data_process['id']) else 'Sending', data_process['id'])
	#写文件
	#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
	data_process.to_csv(path + file_current_name + '\\' + filename + '_' + str(x) + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
	print filename + '_' + str(x) + '-' +file_date + '.csv' + ' ' + 'has finished.'
	print ' '
	if x > 1:
		data_manyidu_offline = data_manyidu_offline.append(data_process)
	else:
		data_manyidu_offline = data_process.iloc[:] #构造满意度用表

#Online-TMALL 部分
data_TMALL_grby = data_TMALL.iloc[:]
data_TMALL_grby = data_TMALL_grby.reset_index(drop = True)
data_TMALL_grby['Flag'] = map(lambda x: 1 if x == 'Sale Order' else -1, data_TMALL_grby['Order Type_I'])
data_TMALL_grby_groupby = data_TMALL_grby.groupby(data_TMALL_grby['Contact or Prospect ID'])['Flag']
data_TMALL_grby_sum = data_TMALL_grby_groupby.sum().reset_index() #groupby重塑
data_TMALL_grby_sum = data_TMALL_grby_sum[data_TMALL_grby_sum['Flag']>0] #取正单
data_TMALL = data_TMALL_grby[data_TMALL_grby['Contact or Prospect ID'].isin(data_TMALL_grby_sum['Contact or Prospect ID'])] #TMALL的所有消费记录
data_TMALL = data_TMALL[(data_TMALL['Order Revenue'] >= 180) & (data_TMALL['Order Revenue'] < 100000)] # 取180-99999 消费记录的人 此处只有 Sale Order的记录了
data_TMALL = data_TMALL.sort_values(by = ['Mobile Phone', 'Order Date', 'Order Id'], ascending = False)
data_TMALL = data_TMALL.drop_duplicates(['Mobile Phone', 'Order Date',]) # 按Mobile Phone, Order Date来去重，取最大一笔订单Order Id(上面一步排序)
data_TMALL['id'] = random.sample(range(len(data_TMALL.index)), len(data_TMALL.index)) 
data_TMALL['Rank_id'] = data_TMALL.groupby(data_TMALL['Mobile Phone'])['Order Date'].rank() # by Mobile Phone by Order Date 组内排序

data_TMALL = data_TMALL.reset_index(drop = True)
con_flag_TMALL = data_TMALL['id']
con_flag_TMALL = sorted(con_flag_TMALL)
#Control组设置
if len(con_flag_TMALL) > (len(con_flag_TMALL) - len(con_flag_TMALL) / 10): # len >= 10时，进行Control组比例设置
	data_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_TMALL[len(con_flag_TMALL) - len(con_flag_TMALL) / 10 ] else 'Sending', data_TMALL['id'])
else: # len < 10时，取id最大的一个值作为control组
	data_TMALL['Control Group'] = map(lambda x: 'Control' if x == max(data_TMALL['id']) else 'Sending', data_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_TMALL.to_csv(path + file_current_name + '\\' + filename + '-' + file_TMALL + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + '-' + file_TMALL + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

#Online-EC 部分
data_EC_grby = data_EC.iloc[:]
data_EC_grby = data_EC_grby.reset_index(drop = True)
data_EC_grby['Flag'] = map(lambda x: 1 if x == 'Sale Order' else -1, data_EC_grby['Order Type_I'])
data_EC_grby_groupby = data_EC_grby.groupby(data_EC_grby['Contact or Prospect ID'])['Flag']
data_EC_grby_sum = data_EC_grby_groupby.sum().reset_index() #groupby重塑
data_EC_grby_sum = data_EC_grby_sum[data_EC_grby_sum['Flag']>0] #取正单
data_EC = data_EC_grby[data_EC_grby['Contact or Prospect ID'].isin(data_EC_grby_sum['Contact or Prospect ID'])] #EC的所有消费记录
data_EC = data_EC[(data_EC['Order Revenue'] >= 180) & (data_EC['Order Revenue'] < 100000)] # 取180-99999 消费记录的人 此处只有 Sale Order的记录了
data_EC = data_EC.sort_values(by = ['Mobile Phone', 'Order Date', 'Order Id'], ascending = False)
data_EC = data_EC.drop_duplicates(['Mobile Phone', 'Order Date',]) # 按Mobile Phone, Order Date来去重，取最大一笔订单Order Id(上面一步排序)
data_EC['id'] = random.sample(range(len(data_EC.index)), len(data_EC.index)) 
data_EC['Rank_id'] = data_EC.groupby(data_EC['Mobile Phone'])['Order Date'].rank() # by Mobile Phone by Order Date 组内排序

data_EC = data_EC.reset_index(drop = True)
con_flag_EC = data_EC['id']
con_flag_EC = sorted(con_flag_EC)
#Control组设置
if len(con_flag_EC) > (len(con_flag_EC) - len(con_flag_EC) / 10): # len >= 10时，进行Control组比例设置
	data_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_EC[len(con_flag_EC) - len(con_flag_EC) / 10 ] else 'Sending', data_EC['id'])
else: # len < 10时，取id最大的一个值作为control组
	data_EC['Control Group'] = map(lambda x: 'Control' if x == max(data_EC['id']) else 'Sending', data_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_EC.to_csv(path + file_current_name + '\\' + filename + '-' + file_EC + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + '-' + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# 满意度用表
data_manyidu_offline['Qudao'] = '线下购买满意度'
data_manyidu_TMALL = data_TMALL.iloc[:]
data_manyidu_TMALL['Qudao'] = flag_month + '月天猫(SMS)'
data_manyidu_EC = data_EC.iloc[:]
data_manyidu_EC['Qudao'] = flag_month + '月官网(SMS)'
data_manyidu = data_manyidu_offline.append(data_manyidu_TMALL)
data_manyidu = data_manyidu.append(data_manyidu_EC)
data_manyidu['Prospect_Flag'] = map(lambda x,y: '新客' if x == y else '老客', data_manyidu['Order Date'], data_manyidu['First Transaction Date(Sale Order)'])
data_manyidu_template = pd.DataFrame(data_manyidu, columns = ['Qudao', 'Mobile Phone','Last Name','Counter Name', 'Order Id', 'Order Date', 'Order Revenue', 'Contact or Prospect ID', 'Counter Employee Login', 'Counter Employee Full Name', 'Amount of Active Card', 'Level Name', 'Prospect_Flag', 'SendingTime', 'Control Group'])
data_manyidu_template['SendingTime'] = SendingTime2
data_manyidu_template = data_manyidu_template[data_manyidu_template['Control Group'] == 'Sending']
data_manyidu_template.to_csv(path + file_current_name + '\\' + filename + '-ZTemplate-Manyidu-' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + '-ZTemplate-Manyidu-' + file_date + ' ' + 'has finished!'

