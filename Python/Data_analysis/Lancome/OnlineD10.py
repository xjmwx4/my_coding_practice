# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: OnlineD10


from pandas import Series, DataFrame
import pandas as pd
import random

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

#读取的文件不能含空格或中文
data_or = pd.read_csv(path + file_current_name + '\OnlineD10.csv', sep = '\t' , encoding = 'utf-16')

#正负单处理
data_or['Flag'] = map(lambda x: 1 if x == 'Sale Order' else -1, data_or['Order Type_I'])
data_or_groupby = data_or.groupby(data_or['ROW_ID'])['Flag']
data_or_sum = data_or_groupby.sum().reset_index() #groupby重塑
data_or_sum = data_or_sum[data_or_sum['Flag']>0] #取正单
data = data_or[data_or['ROW_ID'].isin(data_or_sum['ROW_ID'])]

data = data[data['Points'] >= 200 ] # 留下积分>=200的人进行提醒
#data = data[data['U_Order Revenue'] > 0 ] # 留下金额>0的人进行提醒，即只对Sale Order进行提醒 这句无所谓，因为后面有sort_values by Order Revenue，负值肯定会被踢掉（不存在一个人只有负单没有正单情况）
data = data.reset_index(drop = True) 
data = data.sort_values(by = ['Mobile Phone', 'U_Order Revenue', 'Order Id'], ascending = False) # 保证后续TMALL EC只发一次，筛选规则为取最大一笔金额记录
#data = data.reset_index(drop = True) 
data = data.drop_duplicates(['Mobile Phone']) 	# by 手机号去重，取最大Order Id 不存在一个人对应多个管理柜台情况 不用by ROW_ID
data = data.reset_index(drop = True) 
data['id'] = random.sample(range(len(data.index)), len(data.index)) #随机数生成 注意，当字段超过1W时有可能会报错，增加range范围即可

filename = "OnlineD10"
file_TMALL = '-TMALL'
file_EC = '-EC'
file_date = str(input('Enter File Date: '))
print ' '

#TMALL部分
data_TMALL = data[data['Local Counter Name New'] == 'Lancome TMALL E-commerce']
#删除索引重建
data_TMALL = data_TMALL.reset_index(drop=True) 
con_flag_TMALL = data_TMALL['id']
con_flag_TMALL = sorted(con_flag_TMALL)
#Control组设置
data_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_TMALL[len(con_flag_TMALL) - len(con_flag_TMALL) / 10 ] else 'Sending', data_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_TMALL.to_csv(path + file_current_name + '\\' + filename + file_TMALL + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_TMALL + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_TMALL.to_excel(excel_writer = output_file1, sheet_name = file_date + file_TMALL, index = False, encoding = 'utf-8-sig') #utf-8-sig

#data_TMALL_mp = data_TMALL['Mobile Phone']

#EC 部分
data_EC = data[data['Local Counter Name New'] == 'Lancome E-commerce']
#data_EC = data_EC[ - data_EC['Mobile Phone'].isin(data_TMALL['Mobile Phone'])] 因为有最开始的sort_values by U_Order Revenue，所以可以不用这句
#删除索引重建
data_EC = data_EC.reset_index(drop=True) 
con_flag_EC = data_EC['id']
con_flag_EC = sorted(con_flag_EC)
#Control组设置
data_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_EC[len(con_flag_EC) - len(con_flag_EC) / 10 ] else 'Sending', data_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_EC.to_csv(path + file_current_name + '\\' + filename + file_EC + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_EC.to_excel(excel_writer = output_file1, sheet_name = file_date + file_EC, index = False, encoding = 'utf-8-sig')

