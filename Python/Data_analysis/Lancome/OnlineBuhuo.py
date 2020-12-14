# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: OnlineBuhuo

from pandas import Series, DataFrame
import pandas as pd
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data_M3 = pd.read_csv(path + file_current_name + '\OnlinebuhuoM3.csv', sep = '\t', encoding = 'utf-16')
data_M6 = pd.read_csv(path + file_current_name + '\OnlineM6.csv', sep = '\t', encoding = 'utf-16')
data_M10_or = pd.read_csv(path + file_current_name + '\OnlineM10.csv', sep = '\t', encoding = 'utf-16')
data_M10_exp_point = pd.read(path + file_current_name + '\LAN_EXP_POINT_20171210.csv', encoding = 'utf-8-sig')
data_M12 = pd.read_csv(path + file_current_name + '\OnlineM12.csv', sep = '\t', encoding = 'utf-16')
data_product = pd.read_csv('0LancomeProduct.csv', encoding = 'utf-8-sig')

data_M3_or = pd.merge(data_M3, data_product, left_on = 'Last Order Product SAP Code', right_on = 'SKU', suffixes = ('', '_right'))

filename = 'Online'
file_M3 = '-BuhuoM3'
file_M6 = '-M6'
file_M10 = '-M10'
file_M12 = '-M12'
file_TMALL = '-TMALL'
file_EC = '-EC'
file_flag_skincare = '-SkinCare'
file_flag_makeup = '-Makeup'
file_date = str(input('Enter File Date: '))
print ' '

# drop_duplicates(['Mobile Phone'])后一个人只有一个记录，重复情况：同一个人在TMALL EC各有一笔SkinCare/Makeup记录，而drop_duplicates(['Mobile Phone'])的动作把TMALL EC也去重了
# M3 Skin Care 护肤
data_M3_skincare_or = data_M3_or.loc[data_M3_or['AXE'] == 'Skin Care']
data_M3_skincare = data_M3_skincare_or.iloc[:, 0:3]
data_M3_skincare = data_M3_skincare.drop_duplicates(['Mobile Phone'])
data_M3_skincare['id'] = random.sample(range(len(data_M3_skincare.index)), len(data_M3_skincare.index))
#data_M3_skincare = data_M3_skincare.reset_index(drop = True)

# M3 Make up 彩妆
data_M3_makeup_or = data_M3_or.loc[data_M3_or['AXE'] == 'Make up']
data_M3_makeup = data_M3_makeup_or.iloc[:, 0:3]
data_M3_makeup = data_M3_makeup.drop_duplicates(['Mobile Phone'])
data_M3_makeup = data_M3_makeup[-data_M3_makeup['Mobile Phone'].isin(data_M3_skincare['Mobile Phone'])]
data_M3_makeup['id'] = random.sample(range(len(data_M3_makeup.index)), len(data_M3_makeup.index))
#data_M3_makeup = data_M3_makeup.reset_index(drop = True)

# M3 Skin Care 护肤 TMALL
data_M3_skincare_TMALL = data_M3_skincare[data_M3_skincare['Counter Name New'] == 'ChinaLancome976']
data_M3_skincare_TMALL = data_M3_skincare_TMALL.reset_index(drop = True)
con_flag_M3_skincare_TMALL = data_M3_skincare_TMALL['id']
con_flag_M3_skincare_TMALL = sorted(con_flag_M3_skincare_TMALL)
#Control组设置
data_M3_skincare_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M3_skincare_TMALL[len(con_flag_M3_skincare_TMALL) - len(con_flag_M3_skincare_TMALL) / 10 ] else 'Sending', data_M3_skincare_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M3_skincare_TMALL.to_csv(path + file_current_name + '\\' + filename + file_M3 + file_TMALL + file_flag_skincare + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M3 + file_TMALL + file_flag_skincare + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M3 Skin Care 护肤 EC
data_M3_skincare_EC = data_M3_skincare[data_M3_skincare['Counter Name New'] == 'ChinaLancome986']
data_M3_skincare_EC = data_M3_skincare_EC.reset_index(drop = True)
con_flag_M3_skincare_EC = data_M3_skincare_EC['id']
con_flag_M3_skincare_EC = sorted(con_flag_M3_skincare_EC)
#Control组设置
data_M3_skincare_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M3_skincare_EC[len(con_flag_M3_skincare_EC) - len(con_flag_M3_skincare_EC) / 10 ] else 'Sending', data_M3_skincare_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M3_skincare_EC.to_csv(path + file_current_name + '\\' + filename + file_M3 + file_EC + file_flag_skincare + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M3 + file_EC + file_flag_skincare + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M3 Make up 彩妆 TMALL
data_M3_makeup_TMALL = data_M3_makeup[data_M3_makeup['Counter Name New'] == 'ChinaLancome976']
data_M3_makeup_TMALL = data_M3_makeup_TMALL.reset_index(drop = True)
con_flag_M3_makeup_TMALL = data_M3_makeup_TMALL['id']
con_flag_M3_makeup_TMALL = sorted(con_flag_M3_makeup_TMALL)
#Control组设置
data_M3_makeup_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M3_makeup_TMALL[len(con_flag_M3_makeup_TMALL) - len(con_flag_M3_makeup_TMALL) / 10 ] else 'Sending', data_M3_makeup_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M3_makeup_TMALL.to_csv(path + file_current_name + '\\' + filename + file_M3 + file_TMALL + file_flag_makeup + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M3 + file_TMALL + file_flag_makeup + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M3 Make up 彩妆 EC
data_M3_makeup_EC = data_M3_makeup[data_M3_makeup['Counter Name New'] == 'ChinaLancome986']
data_M3_makeup_EC = data_M3_makeup_EC.reset_index(drop = True)
con_flag_M3_makeup_EC = data_M3_makeup_EC['id']
con_flag_M3_makeup_EC = sorted(con_flag_M3_makeup_EC)
#Control组设置
data_M3_makeup_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M3_makeup_EC[len(con_flag_M3_makeup_EC) - len(con_flag_M3_makeup_EC) / 10 ] else 'Sending', data_M3_makeup_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M3_makeup_EC.to_csv(path + file_current_name + '\\' + filename + file_M3 + file_EC + file_flag_makeup + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M3 + file_EC + file_flag_makeup + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M6
#data_M6 = data_M6.sort_values(by = ['',''],ascending = False)
data_M6 = data_M6.drop_duplicates('Mobile Phone')
data_M10 = data_M10.reset_index(drop = True)
data_M6['id'] = random.sample(range(len(data_M6.index)), len(data_M6.index))

# M6 TMALL
data_M6_TMALL = data_M6[data_M6['Counter Name New'] == 'ChinaLancome976']
data_M6_TMALL = data_M6_TMALL.reset_index(drop = True)
con_flag_M6_TMALL = data_M6_TMALL['id']
con_flag_M6_TMALL = sorted(con_flag_M6_TMALL)
#Control组设置
data_M6_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M6_TMALL[len(con_flag_M6_TMALL) - len(con_flag_M6_TMALL) / 10 ] else 'Sending', data_M6_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M6_TMALL.to_csv(path + file_current_name + '\\' + filename + file_M6 + file_TMALL + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M6 + file_TMALL + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M6 EC
data_M6_EC = data_M6[data_M6['Counter Name New'] == 'ChinaLancome986']
data_M6_EC = data_M6_EC.reset_index(drop = True)
con_flag_M6_EC = data_M6_EC['id']
con_flag_M6_EC = sorted(con_flag_M6_EC)
#Control组设置
data_M6_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M6_EC[len(con_flag_M6_EC) - len(con_flag_M6_EC) / 10 ] else 'Sending', data_M6_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M6_EC.to_csv(path + file_current_name + '\\' + filename + file_M6 + file_EC + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M6 + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M10
data_M10_com = pd.merge(data_M10_or, data_M10_exp_point, how = 'left', left_on = 'Contact or Prospect ID', right_on = 'PERSON_UID', suffixes = ('', '_right'))
data_M10_process = data_M10_com[data_M10_com['EXP_POINT'].notnull()]
data_M10_process.rename(columns={'EXPIRATION_DT':'到期日期', 'EXP_POINT':'到期积分'}, inplace = True) # 可只列出需要修改的列名
data_M10 = pd.DataFrame(data_M10_process, columns = ['Contact or Prospect ID', 'Mobile Phone','Counter Name New','Last Transaction Date(Sale Order)', 'Points', '到期积分', '到期日期'])
data_M10 = data_M10.sort_values(by = ['Mobile Phone','Points'],ascending = False) #还有一种是by 手机号 by Last Transaction Date(Sale Order) 来去重
data_M10 = data_M10.drop_duplicates('Mobile Phone')
data_M10 = data_M10.reset_index(drop = True)
data_M10['id'] = random.sample(range(len(data_M10.index)), len(data_M10.index))

# M10 TMALL
data_M10_TMALL = data_M10[data_M10['Counter Name New'] == 'ChinaLancome976']
data_M10_TMALL = data_M10_TMALL.reset_index(drop = True)
con_flag_M10_TMALL = data_M10_TMALL['id']
con_flag_M10_TMALL = sorted(con_flag_M10_TMALL)
#Control组设置
data_M10_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M10_TMALL[len(con_flag_M10_TMALL) - len(con_flag_M10_TMALL) / 10 ] else 'Sending', data_M10_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M10_TMALL.to_csv(path + file_current_name + '\\' + filename + file_M10 + file_TMALL + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M10 + file_TMALL + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M10 EC
data_M10_EC = data_M10[data_M10['Counter Name New'] == 'ChinaLancome986']
data_M10_EC = data_M10_EC.reset_index(drop = True)
con_flag_M10_EC = data_M10_EC['id']
con_flag_M10_EC = sorted(con_flag_M10_EC)
#Control组设置
data_M10_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M10_EC[len(con_flag_M10_EC) - len(con_flag_M10_EC) / 10 ] else 'Sending', data_M10_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M10_EC.to_csv(path + file_current_name + '\\' + filename + file_M10 + file_EC + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M10 + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'

# M12
data_M12 = data_M12.sort_values(by = ['Mobile Phone','Points'],ascending = False) #还有一种是by 手机号 by Last Transaction Date(Sale Order) 来去重
data_M12 = data_M12.drop_duplicates('Mobile Phone')
data_M12 = data_M12.reset_index(drop = True)
data_M12['id'] = random.sample(range(len(data_M12.index)), len(data_M12.index))

# M12 TMALL
data_M12_TMALL = data_M12[data_M12['Counter Name New'] == 'ChinaLancome976']
data_M12_TMALL = data_M12_TMALL.reset_index(drop = True)
con_flag_M12_TMALL = data_M12_TMALL['id']
con_flag_M12_TMALL = sorted(con_flag_M12_TMALL)
#Control组设置
data_M12_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M12_TMALL[len(con_flag_M12_TMALL) - len(con_flag_M12_TMALL) / 10 ] else 'Sending', data_M12_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M12_TMALL.to_csv(path + file_current_name + '\\' + filename + file_M12 + file_TMALL + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M12 + file_TMALL + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '

# M12 EC
data_M12_EC = data_M12[data_M12['Counter Name New'] == 'ChinaLancome986']
data_M12_EC = data_M12_EC.reset_index(drop = True)
con_flag_M12_EC = data_M12_EC['id']
con_flag_M12_EC = sorted(con_flag_M12_EC)
#Control组设置
data_M12_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_M12_EC[len(con_flag_M12_EC) - len(con_flag_M12_EC) / 10 ] else 'Sending', data_M12_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_M12_EC.to_csv(path + file_current_name + '\\' + filename + file_M12 + file_EC + '-' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_M12 + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'