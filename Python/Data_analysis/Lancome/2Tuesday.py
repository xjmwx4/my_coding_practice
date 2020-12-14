# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: Tuesday files empty writen

from pandas import Series, DataFrame
import pandas as pd
import os
import time

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input the day of today file date (yyyyMMDD): '))
# file_current_name = time.strftime('%Y%m%d',time.localtime(time.time())) # 直接获取当前日期更方便

os.makedirs(path + file_current_name) # 新建名为（当前）日期的文件夹

data1 = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
data2 = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
data3 = pd.DataFrame(columns=['A', 'B', 'C', 'D'])

output_shengri = u'\u0030\u004f\u006e\u006c\u0069\u006e\u0065\u751f\u65e5\u795d\u798f'
output_jiangji_heika = '1' + u'\u964d\u7ea7\u63d0\u9192\u002d\u9ed1\u91d1\u5361'
output_jiangji_jinka = '2' + u'\u964d\u7ea7\u63d0\u9192\u002d\u91d1\u5361'
output_jiangji_yinka1 = '3' + u'\u964d\u7ea7\u63d0\u9192\u002d\u94f6\u5361\u002d\u53ea\u6d88\u8d39\u8fc7\u4e00\u6b21'
output_jiangji_yinka0 = '4' + u'\u964d\u7ea7\u63d0\u9192\u002d\u94f6\u5361\u002d\u672a\u6d88\u8d39\u8fc7'
file_flag_TMALL = 'TMALL'
file_flag_EC = 'EC'
file_flag_heika = u'\u9ed1\u91d1\u5361'
file_flag_jinka = u'\u91d1\u5361'
file_flag_yinka1 = u'\u94f6\u5361\u002d\u53ea\u6d88\u8d39\u8fc7\u0031\u6b21'
file_flag_yinka0 = u'\u94f6\u5361\u002d\u672a\u6d88\u8d39\u8fc7'
#file_date = str(input('Enter File Date (MMDD): '))
print ' '

n = 0

#0生日祝福
writer_shengri = pd.ExcelWriter(path + file_current_name + '\\' + output_shengri + '-' + file_current_name + '.xlsx')
data1.to_excel(writer_shengri, sheet_name = file_flag_TMALL, columns = None, header=False, index = False, encoding = 'utf-8-sig')
data2.to_excel(writer_shengri, sheet_name = file_flag_EC, columns = None, header=False, index = False, encoding = 'utf-8-sig')
writer_shengri.save()
n = n + 1

#1降级提醒-黑金卡
writer_jiangji_heika = pd.ExcelWriter(path + file_current_name + '\\' + output_jiangji_heika + '-' + file_current_name + '.xlsx')
data1.to_excel(writer_jiangji_heika, sheet_name = file_flag_heika, columns = None, header=False, index = False, encoding = 'utf-8-sig')
writer_jiangji_heika.save()
n = n + 1

#2降级提醒-金卡
writer_jiangji_jinka = pd.ExcelWriter(path + file_current_name + '\\' + output_jiangji_jinka + '-' + file_current_name + '.xlsx')
data1.to_excel(writer_jiangji_jinka, sheet_name = file_flag_jinka, columns = None, header=False, index = False, encoding = 'utf-8-sig')
writer_jiangji_jinka.save()
n = n + 1

#3降级提醒-银卡1次
writer_jiangji_yinka1 = pd.ExcelWriter(path + file_current_name + '\\' + output_jiangji_yinka1 + '-' + file_current_name + '.xlsx')
data1.to_excel(writer_jiangji_yinka1, sheet_name = file_flag_yinka1, columns = None, header=False, index = False, encoding = 'utf-8-sig')
writer_jiangji_yinka1.save()
n = n + 1

#4降级提醒-银卡0次
writer_jiangji_yinka0 = pd.ExcelWriter(path + file_current_name + '\\' + output_jiangji_yinka0 + '-' + file_current_name + '.xlsx')
data1.to_excel(writer_jiangji_yinka0, sheet_name = file_flag_yinka0, columns = None, header=False, index = False, encoding = 'utf-8-sig')
writer_jiangji_yinka0.save()
n = n + 1

file_current_date = pd.to_datetime(file_current_name).strftime('%d') # (当前)日期

#OnlineBirthdayMonthly
if file_current_date == '01':
	output_onlinebirthdaymonthly = str(n) + u'\u751f\u65e5\u6708\u002d\u004f\u006e\u006c\u0069\u006e\u0065\u0042\u0069\u0072\u0074\u0068\u0064\u0061\u0079' + '-' + pd.to_datetime(file_current_name).strftime('%m') + u'\u6708'
	writer_onlinebirthdaymonthly = pd.ExcelWriter(path + file_current_name + '\\' + output_onlinebirthdaymonthly + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_onlinebirthdaymonthly, sheet_name = output_onlinebirthdaymonthly, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_onlinebirthdaymonthly.save()
	n = n + 1
else:
	pass

#OfflineBirthday18th
if file_current_date == '18':
	output_offlinebirthday_18 = str(n) + u'\u751f\u65e5\u793c\u7269\u9886\u53d6\u0031\u0038\u0074\u0068' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708'
	print ' '
	output_offline_all_18 = output_offlinebirthday_18 + u'\u002d\u5168\u91cf'
	output_offline_yinkayishang_18 = output_offlinebirthday_18 + u'\u002d\u94f6\u5361\u53ca\u4ee5\u4e0a'
	writer_offline_all_18 = pd.ExcelWriter(path + file_current_name + '\\' + output_offline_all_18 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_offline_all_18, sheet_name = output_offline_all_18, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_offline_all_18.save()
	n = n + 1
	writer_offline_yinkayishang_18 = pd.ExcelWriter(path + file_current_name + '\\' + output_offline_yinkayishang_18 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_offline_yinkayishang_18, sheet_name = output_offline_yinkayishang_18, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_offline_yinkayishang_18.save()
	n = n + 1
else:
	pass

#OfflineBirthday27th
if file_current_date == '27':
	output_offlinebirthday_27 = str(n) + u'\u751f\u65e5\u793c\u7269\u9886\u53d6' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708'
	print ' '
	output_offline_all_27 = output_offlinebirthday_27 + u'\u002d\u5168\u91cf'
	output_offline_yinkayishang_27 = output_offlinebirthday_27 + u'\u002d\u94f6\u5361\u53ca\u4ee5\u4e0a'
	#OfflineBirthdayMonthly
	writer_offline_all_27 = pd.ExcelWriter(path + file_current_name + '\\' + output_offline_all_27 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_offline_all_27, sheet_name = output_offline_all_27, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_offline_all_27.save()
	n = n + 1
	writer_offline_yinkayishang_27 = pd.ExcelWriter(path + file_current_name + '\\' + output_offline_yinkayishang_27 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_offline_yinkayishang_27, sheet_name = output_offline_yinkayishang_27, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_offline_yinkayishang_27.save()
	n = n + 1
else:
	pass

#OfflineBirthday5th
if file_current_date == '05':
	output_offlinebirthday_05 = str(n) + u'\u751f\u65e5\u793c\u7269\u9886\u53d6' + '-' + str(input('Please Enter the Month of the file:')) + u'\u6708' + u'\u8865\u5145\u540d\u5355'
	print ' '
	#OfflineBirthdayMonthly
	writer_offline_all_05 = pd.ExcelWriter(path + file_current_name + '\\' + output_offlinebirthday_05 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_offline_all_05, sheet_name = output_offlinebirthday_05, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_offline_all_05.save()
	n = n + 1
else:
	pass

#Lifecycle M3 M4
if file_current_date == '13' or file_current_date == '26' :
	output_lifecycleM3 = str(n) + 'Lifecycle_M3'
	writer_lifecycleM3 = pd.ExcelWriter(path + file_current_name + '\\' + output_lifecycleM3 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_lifecycleM3, sheet_name = output_lifecycleM3, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_lifecycleM3.save()
	n = n + 1
	output_lifecycleM4 = str(n) + 'Lifecycle_M4'
	writer_lifecycleM4 = pd.ExcelWriter(path + file_current_name + '\\' + output_lifecycleM4 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_lifecycleM4, sheet_name = output_lifecycleM4, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_lifecycleM4.save()
	n = n + 1
else:
	pass

#OnlineM3 补货 OnlineM6 OnlineM10 OnlineM12
if file_current_date == '15':
	output_onlineM3 = str(n) + u'\u004f\u006e\u006c\u0069\u006e\u0065\u004d\u0033\u002d\u8865\u8d27\u901a\u77e5'
	writer_onlineM3 = pd.ExcelWriter(path + file_current_name + '\\' + output_onlineM3 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_onlineM3, sheet_name = output_onlineM3, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_onlineM3.save()
	n = n + 1
	output_onlineM6 = str(n) + 'OnlineM6'
	writer_onlineM6 = pd.ExcelWriter(path + file_current_name + '\\' + output_onlineM6 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_onlineM6, sheet_name = output_onlineM6, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_onlineM6.save()
	n = n + 1
	output_onlineM10 = str(n) + 'OnlineM10'
	writer_onlineM10 = pd.ExcelWriter(path + file_current_name + '\\' + output_onlineM10 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_onlineM10, sheet_name = output_onlineM10, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_onlineM10.save()
	n = n + 1
	output_onlineM12 = str(n) + 'OnlineM12'
	writer_onlineM12 = pd.ExcelWriter(path + file_current_name + '\\' + output_onlineM12 + '-' + file_current_name + '.xlsx')
	data1.to_excel(writer_onlineM12, sheet_name = output_onlineM12, columns = None, header=False, index = False, encoding = 'utf-8-sig')
	writer_onlineM12.save()
	n = n + 1
else:
	pass

print 'Files of Tuesday All Finished!'