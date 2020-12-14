# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: WechatSatisfaction

from pandas import Series, DataFrame
import pandas as pd
import random
import math
import timeit

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

start = timeit.default_timer()
data = pd.read_csv(path + file_current_name + '\WechatSatisfaction.csv', sep = '\t', encoding = 'utf-16', low_memory = False)
time_point_1 = timeit.default_timer()
print 'Running Time of Processing: ', time_point_1 - start
print ' '

filename = "Wechat_Satisfaction"
file_date = str(input('Enter File Date (MMDD): '))
SendingTime = input('Input SendingTime Date(str'' yyyyMMDD yinhao): ')
SendingTime2 = pd.to_datetime(SendingTime).strftime('%Y/%m/%d')
print ' '

data['Customer_Flag'] = map(lambda x,y: '新客' if x == y else '老客', data['First Transaction Date(Sale Order)'], data['Order Date'])

data_satisfaction = pd.DataFrame(data, columns = ['渠道', 'Mobile Phone','Last Name','Counter Name', 'Order Id', 'Order Date', 'Order Revenue', 'Contact or Prospect ID', 'Counter Employee Login', 'Counter Employee Full Name', 'Amount of Active Card', 'Level Name', 'Customer_Flag', 'SendingTime'])
data_satisfaction['渠道'] = '微信端消费满意度调查'
data_satisfaction['SendingTime'] = SendingTime2
data_satisfaction['Counter Employee Full Name'] = map(lambda x: x.replace(', -', ''), data_satisfaction['Counter Employee Full Name'])
time_point_2 = timeit.default_timer()
print 'Running Time of Processing: ', time_point_2 - time_point_1
print ' '

data_satisfaction.columns = ['渠道', '手机号', '姓名', '柜台编号', '订单ID', '订单时间', '交易金额','会员编号', 'BAID', 'BA姓名', '年消费', '等级', '新/老/潜客', '发送时间'] # 所有列都必须列出来

time_point_3 = timeit.default_timer()
print 'Running Time of Processing: ', time_point_3 - time_point_2
print ' '
data_satisfaction = data_satisfaction.sort_values(by = ['手机号', '订单时间', '订单ID'], ascending = False)
data_satisfaction = data_satisfaction.drop_duplicates(['手机号', '订单时间'])
data_satisfaction = data_satisfaction.reset_index(drop = True)

time_point_4 = timeit.default_timer()
print 'Running Time of Processing: ', time_point_4 - time_point_3
print ' '

data_satisfaction.to_csv(path + file_current_name + '\\' + filename + '_' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
time_point_5 = timeit.default_timer()
print 'Running Time of Writing file: ', time_point_5 - time_point_4
