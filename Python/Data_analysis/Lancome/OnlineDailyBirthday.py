# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: OnlineDailyBirthday
# remark: 还是在于格式保存的问题，因为写入excel有问题，所以暂时选择保存为csv

from pandas import Series, DataFrame
import pandas as pd
import random

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

#读取的文件不能含空格或中文
data = pd.read_csv(path + file_current_name + '\OnlineDailyBirthday.csv', sep = '\t' , encoding = 'utf-16')
# 将Birthday转化为标准日期格式 1990/09/22 00:00:00
#data['Birthday'] = pd.to_datetime(data['Birthday'])


#数据前期处理
#调整日期格式 yy/MM/DD hh:mm:ss

#会员等级处理 新增 Level_Number 字段
#data['Level_Number'] = map(lambda x: 0 if x = 'GC' else 1 if x = u'\u666e\u901a\u4f1a\u5458' else 2 if x = u'\u94f6\u5361\u4f1a\u5458' else 3 if x = u'\u91d1\u5361\u4f1a\u5458' else 4 if x = u'\u9ed1\u91d1\u5361\u4f1a\u5458' else -1, data['Level Name'])

data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Level Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

#随机数生成
data['id'] = random.sample(range(len(data.index)), len(data.index)) #	注：当len(data.index)>range的10000时，会报错，错误类型：sample larger than population
#去重处理
#data.duplicated() #判断是否有重复
#data.drop_duplicates(['k2']) #去重指定列（留下index小的）
data = data.sort_values(by = ['Mobile Phone', 'Level_Number'], ascending = False)
data = data.reset_index(drop = True)
data = data.drop_duplicates(['Mobile Phone'])
data = data.sort_values(by = 'Mobile Phone', ascending = True)
data = data.reset_index(drop = True)

#Control组设置部分
#data['id'] = random.sample(range(10000), len(data.index))
#con_flag = data['id']
#con_flag = sorted(con_flag)

#TMALL data[data['Counter Name New'] == 'ChinaLancome976']
#EC data[data['Counter Name New'] == 'ChinaLancome986']

#整体步骤
#data['Control Group'] = map(lambda x: 'Control' if x>=con_flag[len(con_flag) - len(con_flag) / 10 ] else 'Sending', data['id'])
#filename = "OnlineDailyBirthday_sig-1101.csv"
#data.to_csv(filename, index = False, encoding = 'utf-8-sig')


filename = "OnlineDailyBirthday"
file_TMALL = '-TMALL'
file_EC = '-EC'
file_date = str(input('Enter File Date (MMDD): '))
print ' '
#output_file = pd.ExcelWriter(filename + file_date + '.xlsx')
#不知道为什么，如果事先不做好字符串的连接，excel无法生成（不能在to_excel里面进行拼接字符串）
#sheet_TMALL = file_date + file_TMALL
#sheet_EC = file_date + file_EC
#out_filename = filename + '-' + file_date + '.xlsx'
#output_file = pd.ExcelWriter(out_filename)
#output_file1 = pd.ExcelWriter(filename + '-' + file_date + '.xlsx')

#TMALL 部分
data_TMALL = data[data['Counter Name New'] == 'ChinaLancome976']
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

#EC 部分
data_EC = data[data['Counter Name New'] == 'ChinaLancome986']
#删除索引重建
data_EC = data_EC.reset_index(drop=True) 
con_flag_EC = data_EC['id']
con_flag_EC = sorted(con_flag_EC)
#Control组设置
data_EC['Control Group'] = map(lambda x: 'Control' if x>=con_flag_EC[len(con_flag_EC) - len(con_flag_EC) / 10 ] else 'Sending', data_EC['id'])
#写文件
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data_EC.to_csv(path + file_current_name + '\\' + filename + file_EC + ' ' +file_date + '.csv', index = False, encoding = 'utf-8-sig')
print filename + file_EC + '-' +file_date + '.csv' + ' ' + 'has finished.'
print ' '
#data_EC.to_excel(excel_writer = output_file1, sheet_name = file_date + file_EC, index = False, encoding = 'utf-8-sig')



#def csv_to_xlsx_pd():
#    csv = pd.read_csv(filename, encoding = 'utf-8-sig')
#    csv.to_excel('OnlineDailyBirthday_sig-1101.xlsx', sheet_name='OnlineDailyBirthday-1101', index = False, encoding = 'utf-8-sig')


#if __name__ == '__main__':
#    csv_to_xlsx_pd()

