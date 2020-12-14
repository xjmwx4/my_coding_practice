# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: BirthdayMonthly-Online

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\BirthdayMonthly.csv', sep = '\t', encoding = 'utf-16')

#会员等级处理 新增 Level_Number 字段
data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Level Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

data = data.sort_values(by = ['Contact or Prospect ID', 'Mobile Phone', 'Level_Number'], ascending = False)
data = data.drop_duplicates(['Contact or Prospect ID', 'Mobile Phone'])
data = data.reset_index(drop = True)

#PCG人群标记，取TMALL EC人群，取手机号为11位
data['PCG_Flag'] = map(lambda x,y: 'Y' if (pd.isnull(x) == False and pd.isnull(y) == True) else 'N', data['Pure Control Flag'], data['Pure Control Real Remain Date']) 
data = data[data['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986'])]
data['Phone_Flag'] = map(lambda x: True if len(str(x)) == 11 else False, data['Mobile Phone'])
data = data[data['Phone_Flag'] == True]

data['id'] = random.sample(range(len(data.index)), len(data.index)) #随机数生成 注意，当字段超过1W时有可能会报错，增加range范围即可

filename = "BirthdayMonthly-Online"
tag1 = '-YinkaPuka'
tag2 = '-HeikaJinka'
file_TMALL = '-TMALL'
file_EC = '-EC'
file_date = str(input('Enter File Date: '))
print ' '

#银卡普卡 TMALL
data_yinkapuka_TMALL = data[((data['Level Name'] == u'\u666e\u901a\u4f1a\u5458') | (data['Level Name'] == u'\u94f6\u5361\u4f1a\u5458')) & (data['Counter Name New'] == 'ChinaLancome976')]
#删除索引重建
data_yinkapuka_TMALL = data_yinkapuka_TMALL.reset_index(drop=True) 
con_flag_yinkapuka_TMALL = data_yinkapuka_TMALL['id']
con_flag_yinkapuka_TMALL = sorted(con_flag_yinkapuka_TMALL)
#Control组设置
data_yinkapuka_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_yinkapuka_TMALL[len(con_flag_yinkapuka_TMALL) - len(con_flag_yinkapuka_TMALL) / 10 ] else 'Sending', data_yinkapuka_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_yinkapuka_TMALL.to_csv(path + file_current_name + '\\' + filename + tag1 + file_TMALL + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + tag1 + file_TMALL + '-' + file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_yinkapuka_TMALL.to_excel(excel_writer = output_file1, sheet_name = file_date + file_TMALL, index = False, encoding = 'utf-8-sig') #utf-8-sig

#银卡普卡 EC
data_yinkapuka_EC = data[((data['Level Name'] == u'\u666e\u901a\u4f1a\u5458') | (data['Level Name'] == u'\u94f6\u5361\u4f1a\u5458')) & (data['Counter Name New'] == 'ChinaLancome986')]
#删除索引重建
data_yinkapuka_EC = data_yinkapuka_EC.reset_index(drop=True) 
con_flag_yinkapuka_EC = data_yinkapuka_EC['id']
con_flag_yinkapuka_EC = sorted(con_flag_yinkapuka_EC)
#Control组设置
data_yinkapuka_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_yinkapuka_EC[len(con_flag_yinkapuka_EC) - len(con_flag_yinkapuka_EC) / 10 ] else 'Sending', data_yinkapuka_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_yinkapuka_EC.to_csv(path + file_current_name + '\\' + filename + tag1 + file_EC + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + tag1 + file_EC + '-' + file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_yinkapuka_TMALL.to_excel(excel_writer = output_file1, sheet_name = file_date + file_TMALL, index = False, encoding = 'utf-8-sig') #utf-8-sig

#黑卡金卡 TMALL
data_heikajinka_TMALL = data[((data['Level Name'] == u'\u91d1\u5361\u4f1a\u5458') | (data['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458')) & (data['Counter Name New'] == 'ChinaLancome976')]
#删除索引重建
data_heikajinka_TMALL = data_heikajinka_TMALL.reset_index(drop=True) 
con_flag_heikajinka_TMALL = data_heikajinka_TMALL['id']
con_flag_heikajinka_TMALL = sorted(con_flag_heikajinka_TMALL)
#Control组设置
data_heikajinka_TMALL['Control Group'] = map(lambda x: 'Control' if x>=con_flag_heikajinka_TMALL[len(con_flag_heikajinka_TMALL) - len(con_flag_heikajinka_TMALL) / 10 ] else 'Sending', data_heikajinka_TMALL['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_heikajinka_TMALL.to_csv(path + file_current_name + '\\' + filename + tag2 + file_TMALL + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + tag2 + file_TMALL + '-' + file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_yinkapuka_TMALL.to_excel(excel_writer = output_file1, sheet_name = file_date + file_TMALL, index = False, encoding = 'utf-8-sig') #utf-8-sig

#黑卡金卡 EC
data_heikajinka_EC = data[((data['Level Name'] == u'\u91d1\u5361\u4f1a\u5458') | (data['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458')) & (data['Counter Name New'] == 'ChinaLancome986')]
#删除索引重建
data_heikajinka_EC = data_heikajinka_EC.reset_index(drop=True) 
con_flag_heikajinka_EC = data_heikajinka_EC['id']
con_flag_heikajinka_EC = sorted(con_flag_heikajinka_EC)
#Control组设置
data_heikajinka_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_heikajinka_EC[len(con_flag_heikajinka_EC) - len(con_flag_heikajinka_EC) / 10 ] else 'Sending', data_heikajinka_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_heikajinka_EC.to_csv(path + file_current_name + '\\' + filename + tag2 + file_EC + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + tag2 + file_EC + '-' + file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_yinkapuka_TMALL.to_excel(excel_writer = output_file1, sheet_name = file_date + file_TMALL, index = False, encoding = 'utf-8-sig') #utf-8-sig
