# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: Prospect


from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import random
import math

print 'Please prepare the files below :'
print '1.xiaoheiban data, xiaoheiban-filedate'
print '2.D7 D21 files.(Created by previous).Use Directly.'
print '3.PURCHASE-D3-filedate'
print '4.PURCHASE-D7-filedate'
print ' '
print 'or Please enter Ctrl + C to end, and to prepare these files.'

#设置文件读取路径，直接从文件目录读取，注意转义问题
#path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
path = 'C:\Users\Administrator\python1208\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

filename = 'Prospect'
file_D3 = '-D3'
file_D7 = '-D7'
file_D21 = '-D21'
file_flag_service = '-Service'
file_flag_sample = '-Sample'
file_date = str(input('Enter File Date: '))
SendingTime = input('Enter SendingTime Date(str'' yyyyMMDD yinhao): ')
SendingTime2 = pd.to_datetime(SendingTime).strftime('%Y/%m/%d')

data_buy = pd.read_csv(path + file_current_name + '\OfflineOnlineD3.csv', sep = '\t', encoding = 'utf-16')
data_D3 = pd.read_csv(path + file_current_name + '\ProspectD3.csv', sep = '\t', encoding = 'utf-16')
data_birthday = pd.read_csv(path + file_current_name + '\\' + 'xiaoheiban-' + file_date + '.csv', encoding = 'utf-8-sig')
data_birthday[u'验证时间'] = map(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d 00:00:00') if pd.isnull(x) == False else x, data_birthday[u'验证时间']) #调整时间格式
data_buy_D3 = pd.read_csv(path + file_current_name + '\\' + 'PURCHASE_D3_' + file_current_name + '.csv', encoding = 'ascii')
data_buy_D7 = pd.read_csv(path + file_current_name + '\\' + 'PURCHASE_D7_' + file_current_name + '.csv', encoding = 'ascii')
data_D3['Counter Employee Full Name'] = map(lambda x: x.replace(', -', '') if pd.isnull(x) == False else x, data_D3['Counter Employee Full Name']) # BA Name部分字符串处理

#Prospect名条中剔掉当天有过购买记录的人，一天一个人只收到一条满意度短信
data_buy = data_buy[data_buy['Order Revenue'] != 0]
data_buy['Flag'] = map(lambda x: 1 if x == 'Sale Order' else -1, data_buy['Order Type_I'])
data_buy_groupby = data_buy.groupby(data_buy['Contact or Prospect ID'])['Flag']
data_buy_sum = data_buy_groupby.sum().reset_index() #groupby重塑
data_buy_sum = data_buy_sum[data_buy_sum['Flag']>0] #取正单
data_buy_zhengdan = data_buy[data_buy['Contact or Prospect ID'].isin(data_buy_sum['Contact or Prospect ID'])]
data_buy_zhengdan = data_buy_zhengdan[(data_buy_zhengdan['Order Revenue'] >= 180) & (data_buy_zhengdan['Order Revenue'] < 100000)] # 取180-99999 消费记录的人 此处只有 Sale Order的记录了
data_buy_zhengdan = data_buy_zhengdan.sort_values(by = ['Mobile Phone', 'Order Date', 'Order Id'], ascending = False)
data_buy_zhengdan = data_buy_zhengdan.drop_duplicates(['Mobile Phone', 'Order Date',]) # 按Mobile Phone, Order Date来去重，取最大一笔订单Order Id(上面一步排序)
data = pd.merge(data_D3, data_buy_zhengdan, how = 'left', on = ['Mobile Phone', 'Order Date'], suffixes = ('', '_right'))
data = data[data['Contact or Prospect ID_right'].isnull()] #剔掉购买记录正单的人,即取left join为空的部分，非空部分为与购买记录相匹配
data_D3_or = data.iloc[:,0:14]
data_D3_or = data_D3_or.reset_index(drop = True)

# D3 Service
data_D3_service = data_D3_or[data_D3_or['SAP Code'] == 'service' ]
data_D3_service = data_D3_service.sort_values(by = ['Mobile Phone', 'Order Id'], ascending = False)
data_D3_service = data_D3_service.drop_duplicates(['Mobile Phone'])#'Contact or Prospect ID', 
data_D3_service = data_D3_service.reset_index(drop = True)
data_D3_service['Prospect_Flag'] = map(lambda x: 'For Prospect' if pd.isnull(x) == True else 'No Order', data_D3_service['First Transaction Date(Sale Order)'])
data_D3_service['id'] = random.sample(range(len(data_D3_service.index)), len(data_D3_service.index))
con_flag_D3_service = data_D3_service['id']
con_flag_D3_service = sorted(con_flag_D3_service)
#Control组设置
data_D3_service['Control Group'] = map(lambda x: 'Control' if x>=con_flag_D3_service[len(con_flag_D3_service) - len(con_flag_D3_service) / 10 ] else 'Sending', data_D3_service['id'])
data_D3_service.to_csv(path + file_current_name + '\\' + filename + file_D3 + file_flag_service + '-' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print filename + file_D3 + file_flag_service + '-' + file_date + ' ' + 'has finished!'

# D3 Service 满意度 template用表
#data_D3_service_template = pd.DataFrame(data_D3_service, columns = ['Qudao', 'Mobile Phone','Last Name','Counter Name', 'Order Id', 'Order Date', 'Order Revenue', 'Contact or Prospect ID', 'Counter Employee Login', 'Counter Employee Full Name', 'Amount of Active Card', 'Level Name', 'Prospect_Flag', 'SendingTime', 'Control Group'])
#data_D3_service_template['Qudao'] = '线下体验满意度（SMS）'
#data_D3_service_template['Prospect_Flag'] = map(lambda x: '潜客' if x == 'For Prospect' else '老客', data_D3_service_template['Prospect_Flag'])
#data_D3_service_template['SendingTime'] = SendingTime2
#data_D3_service_template = data_D3_service_template[data_D3_service_template['Control Group'] == 'Sending']
#data_D3_service_template.to_csv(path + file_current_name + '\\' + filename + file_D3 + file_flag_service + '-Template ' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
#print ''
#print filename + file_D3 + file_flag_service + ' Template ' + file_date + ' ' + 'has finished!'

# D3 Sample
data_D3_sample = data_D3_or[data_D3_or['SAP Code'] != 'service' ]
data_D3_sample = data_D3_sample.sort_values(by = ['Mobile Phone', 'Order Id'], ascending = False)
data_D3_sample = data_D3_sample.drop_duplicates(['Mobile Phone'])#'Contact or Prospect ID', 
data_D3_sample['Prospect_Flag'] = map(lambda x: 'For Prospect' if pd.isnull(x) == True else 'No Order', data_D3_sample['First Transaction Date(Sale Order)'])
data_D3_sample_com = pd.merge(data_D3_sample, data_birthday, how = 'left', left_on = ['Mobile Phone', 'Order Date'], right_on = [u'手机', u'验证时间'], suffixes = ('', '_right'))	# 合并生日礼记录
data_D3_sample_com = data_D3_sample_com[data_D3_sample_com[u'手机'].isnull()] # 剔掉生日礼的人(需要其手机号、日期都能匹上才算生日礼的人)
data_D3_sample = data_D3_sample_com.iloc[:,0:15]
data_D3_sample = data_D3_sample[-data_D3_sample['Mobile Phone'].isin(data_D3_service['Mobile Phone'])] # 去掉服务的人，同一批发短信的人，优先服务
data_D3_sample = data_D3_sample.reset_index(drop = True)
data_D3_sample['id'] = random.sample(range(len(data_D3_sample.index)), len(data_D3_sample.index))
con_flag_D3_sample = data_D3_sample['id']
con_flag_D3_sample = sorted(con_flag_D3_sample)
#Control组设置
data_D3_sample['Control Group'] = map(lambda x: 'Control' if x>=con_flag_D3_sample[len(con_flag_D3_sample) - len(con_flag_D3_sample) / 10 ] else 'Sending', data_D3_sample['id'])
data_D3_sample.to_csv(path + file_current_name + '\\' + filename + file_D3 + file_flag_sample + '-' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print filename + file_D3 + file_flag_sample + '-' + file_date + ' ' + 'has finished!'

# D3 Service & Sample 满意度 template用表 (已合并为一个文件)
data_D3_service['Qudao'] = '线下体验满意度（SMS）'
data_D3_sample['Qudao'] = '线下小样领用满意度（SMS）'
data_D3_manyidu = data_D3_service.append(data_D3_sample)
data_D3_manyidu_template = pd.DataFrame(data_D3_manyidu, columns = ['Qudao', 'Mobile Phone','Last Name','Counter Name', 'Order Id', 'Order Date', 'Order Revenue', 'Contact or Prospect ID', 'Counter Employee Login', 'Counter Employee Full Name', 'Amount of Active Card', 'Level Name', 'Prospect_Flag', 'SendingTime', 'Control Group'])
data_D3_manyidu_template['Prospect_Flag'] = map(lambda x: '潜客' if x == 'For Prospect' else '老客', data_D3_manyidu_template['Prospect_Flag'])
data_D3_manyidu_template['Amount of Active Card'] = map(lambda x,y: '' if x == '潜客' else y, data_D3_manyidu_template['Prospect_Flag'], data_D3_manyidu_template['Amount of Active Card']) # 去掉潜客的年消费和会员等级，保留老客的
data_D3_manyidu_template['Level Name'] = map(lambda x,y: '' if x == '潜客' else y, data_D3_manyidu_template['Prospect_Flag'], data_D3_manyidu_template['Level Name']) # 去掉潜客的年消费和会员等级，保留老客的
data_D3_manyidu_template['SendingTime'] = SendingTime2
data_D3_manyidu_template = data_D3_manyidu_template[data_D3_manyidu_template['Control Group'] == 'Sending']
data_D3_manyidu_template = data_D3_manyidu_template.reset_index(drop = True)
data_D3_manyidu_template.to_csv(path + file_current_name + '\\' + filename + file_D3 + '-Manyidu' + '-Template ' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print filename + file_D3 + '-Manyidu' + '-Template-' + file_date + ' ' + 'has finished!'

#看看日期部分能不能有个规律，直接采用已有数据计算而非手动输入
# D7 Sample
file_date_name_lastloop_D3 = str(input('Please enter the last loop D3 sample file date: '))
data_D3_sample_lastloop = pd.read_csv(path + file_current_name + '\\' + filename + file_D3 + file_flag_sample + '-' + file_date_name_lastloop_D3 + '.csv', encoding = 'utf-8-sig')
data_D3_sample_lastloop = data_D3_sample_lastloop[data_D3_sample_lastloop['Control Group'] == 'Sending']
data_D3_sample_lastloop = data_D3_sample_lastloop.reset_index(drop=True)
data_D3_sample_lastloop_sending = data_D3_sample_lastloop.iloc[:,0:14] # 选择前15列数据作为D7的源数据
data_D7_sample = data_D3_sample_lastloop_sending.iloc[:]
data_D7_sample_com = pd.merge(data_D7_sample, data_birthday, how = 'left', left_on = ['Mobile Phone', 'Order Date'], right_on = [u'手机', u'验证时间'], suffixes = ('', '_right'))	# 合并生日礼记录
data_D7_sample = data_D7_sample_com[data_D7_sample_com[u'手机'].isnull()] # 剔掉生日礼的人(需要其手机号、日期都能匹上才算生日礼的人)
data_D7_sample = data_D7_sample[-data_D7_sample['ROW_ID'].isin(data_buy_D3['customer_id'])] # 去掉有购买记录的人
data_D7_sample = data_D7_sample.reset_index(drop = True)
data_D7_sample['id'] = random.sample(range(len(data_D7_sample.index)), len(data_D7_sample.index))
con_flag_D7_sample = data_D7_sample['id']
con_flag_D7_sample = sorted(con_flag_D7_sample)
#Control组设置
data_D7_sample['Control Group'] = map(lambda x: 'Control' if x>=con_flag_D7_sample[len(con_flag_D7_sample) - len(con_flag_D7_sample) / 10 ] else 'Sending', data_D7_sample['id'])
data_D7_sample.to_csv(path + file_current_name + '\\' + filename + file_D7 + '-' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print filename + file_D7 + '-' + file_date + ' ' + 'has finished!'

# data_D7_sample['Order Date'] = map(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d 00:00:00') if pd.isnull(x) == False else x, data_D7_sample['Order Date']) #	格式的调整

#看看日期部分能不能有个规律，直接采用已有数据计算而非手动输入
# D21 Sample
file_date_name_lastloop_D7 = str(input('Please enter the last loop D7 sample file date: '))
data_D7_sample_lastloop = pd.read_csv(path + file_current_name + '\\' + filename + file_D7 + '-' + file_date_name_lastloop_D7 + '.csv', encoding = 'utf-8-sig')
data_D7_sample_lastloop = data_D7_sample_lastloop[data_D7_sample_lastloop['Control Group'] == 'Sending']
data_D7_sample_lastloop = data_D7_sample_lastloop.reset_index(drop=True)
data_D7_sample_lastloop_sending = data_D7_sample_lastloop.iloc[:,0:14] # 选择前15列数据作为D7的源数据
data_D21_sample = data_D7_sample_lastloop_sending.iloc[:]
data_D21_sample_com = pd.merge(data_D21_sample, data_birthday, how = 'left', left_on = ['Mobile Phone', 'Order Date'], right_on = [u'手机', u'验证时间'], suffixes = ('', '_right'))	# 合并生日礼记录
data_D21_sample = data_D21_sample_com[data_D21_sample_com[u'手机'].isnull()] # 剔掉生日礼的人(需要其手机号、日期都能匹上才算生日礼的人)
data_D21_sample = data_D21_sample[-data_D21_sample['ROW_ID'].isin(data_buy_D7['customer_id'])] # 去掉有购买记录的人
data_D21_sample = data_D21_sample.reset_index(drop = True)
data_D21_sample['id'] = random.sample(range(len(data_D21_sample.index)), len(data_D21_sample.index))
con_flag_D21_sample = data_D21_sample['id']
con_flag_D21_sample = sorted(con_flag_D21_sample)
#Control组设置
data_D21_sample['Control Group'] = map(lambda x: 'Control' if x>=con_flag_D21_sample[len(con_flag_D21_sample) - len(con_flag_D21_sample) / 10 ] else 'Sending', data_D21_sample['id'])
data_D21_sample.to_csv(path + file_current_name + '\\' + filename + file_D21 + '-' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print filename + file_D21 + '-' + file_date + ' ' + 'has finished!'