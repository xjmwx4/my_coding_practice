# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: NewJoin


from pandas import Series, DataFrame
import pandas as pd
import random

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\Newupdate.csv', sep = '\t', encoding = 'utf-16')
data_history = pd.read_csv(path + file_current_name + '\Levelhistory.csv', sep = '\t', encoding = 'utf-16')

data['id'] = random.sample(range(len(data.index)), len(data.index)) 	#新增随机数id列

filename = "Newupdate"
file_heika0 = '-Heijinka0' # for new update
file_heika1 = '-Heijinka1' # for 续会 & 降级又升级
file_yinka = '-Yinka'
file_date = str(input('Enter File Date: '))
print ' '

#黑卡新升级部分
data_heika0 = data[data['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458']
#删除索引重建
data_heika0 = data_heika0.reset_index(drop=True) 
con_flag_heika0 = data_heika0['id']
con_flag_heika0 = sorted(con_flag_heika0)
#Control组设置
data_heika0['Control Group'] = map(lambda x: 'Control' if x>=con_flag_heika0[len(con_flag_heika0) - len(con_flag_heika0) / 10 ] else 'Sending', data_heika0['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_heika0.to_csv(path + file_current_name + '\\' + filename + file_heika0 + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_heika0 + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_heika.to_excel(excel_writer = output_file1, sheet_name = file_date + file_heika0, index = False, encoding = 'utf-8-sig') #utf-8-sig

#黑卡续会&降级又升级部分 黑卡1有毒。。。
data_heika1 = data[data['Level Name'] == u'\u9ed1\u91d1\u5361\u4f1a\u5458']
data_heika1_merge = pd.merge(data_heika1, data_history, how = 'inner', on = ['Contact or Prospect ID', 'Level Name'], suffixes = ('', '_right'))
data_heika1_final = data_heika1_merge.iloc[:, 0:7] 	# 只留原Newupdate表的字段，连接后的字段忽略

con_flag_heika1 = data_heika1_final['id']
con_flag_heika1 = sorted(con_flag_heika1)
#Control组设置
data_heika1_final['Control Group'] = map(lambda x: 'Control' if x>=con_flag_heika1[len(con_flag_heika1) - len(con_flag_heika1) / 10 ] else 'Sending', data_heika1_final['id'])
#写文件
data_heika1_final.to_csv(path + file_current_name + '\\' + filename + file_heika1 + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_heika1 + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_heika.to_excel(excel_writer = output_file1, sheet_name = file_date + file_yinka, index = False, encoding = 'utf-8-sig') #utf-8-sig


#银卡续会&降级又升级部分
data_yinka = data[data['Level Name'] == u'\u94f6\u5361\u4f1a\u5458']
data_yinka_merge = pd.merge(data_yinka, data_history, how = 'inner', on = ['Contact or Prospect ID', 'Level Name'], suffixes = ('', '_right'))
data_yinka_final = data_yinka_merge.iloc[:, 0:7] 	# 只留原Newupdate表的字段，连接后的字段忽略

con_flag_yinka = data_yinka_final['id']
con_flag_yinka = sorted(con_flag_yinka)
#Control组设置
data_yinka_final['Control Group'] = map(lambda x: 'Control' if x>=con_flag_yinka[len(con_flag_yinka) - len(con_flag_yinka) / 10 ] else 'Sending', data_yinka_final['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_yinka_final.to_csv(path + file_current_name + '\\' + filename + file_yinka + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_yinka + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_heika.to_excel(excel_writer = output_file1, sheet_name = file_date + file_yinka, index = False, encoding = 'utf-8-sig') #utf-8-sig
