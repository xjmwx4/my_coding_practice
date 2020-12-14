# -*- conding:utf8 -*-


from pandas import DataFrame,Series
import pandas as pd
import math
import timeit


path = 'D:\\Otype-Fitz.Xu\\Lorealparis\\Lancome\\2Assign\\WechatGroupby'
file_current_name = str(input('Please input current file date (MMDD): '))

#基本思路，先对微信匹配表进行by openid by date排序，重置下index，然后by openid 去重，留下index最小的值
start = timeit.default_timer()
df_origin = pd.read_csv(path + file_current_name + '\ms_member20171204.csv', sep = '\t', encoding = 'utf-16')
df_wechat_com = pd.read_csv(path + file_current_name + '\WechatCom20171205.csv', sep = '\t', encoding = 'utf-16')
break_point_1 = timeit.default_timer()
print 'Break point 1 :', break_point_1 - start

df_wechat_com_sort = df_wechat_com.sort_values(by = ['Social Network ID', 'Last Transaction Date(Sale Order)'], ascending = False)
df_wechat_com_sort = df_wechat_com_sort.reset_index(drop = True)
df_wechat_com_sort = df_wechat_com_sort.drop_duplicates(['Social Network ID'])
df_wechat_com_sort = df_wechat_com_sort.reset_index(drop = True)
break_point_2 = timeit.default_timer()
print 'Break point 2 :', break_point_2 - break_point_1

#LEFT JOIN后结果，一一对应表
df_com = pd.merge(df_origin, df_wechat_com_sort, how = 'left', left_on = 'openid', right_on = 'Social Network ID')
df_com_final = df_com[['membersid', 'mobile', 'openid', 'marsid', 'Counter Name New']]
df_com_final_notnull = df_com_final[df_com_final['Counter Name New'].notnull()] 	# 新建一个非空值的表，用于之后使用
break_point_3 = timeit.default_timer()
print 'Break point 3 :', break_point_3 - break_point_2

#Online+非绑会员
df_com_TMALL = df_com_final[df_com_final['Counter Name New'] == 'ChinaLancome976']
df_com_EC = df_com_final[df_com_final['Counter Name New'] == 'ChinaLancome986']
df_com_null_0 = pd.isnull(df_com_final['Counter Name New'])
df_com_null = df_com_final[df_com_null_0 == True]
break_point_4 = timeit.default_timer()
print 'Break point 4 :', break_point_4 - break_point_3

#Online部分
df_com_online_1 = df_com_TMALL.append(df_com_EC)
#到此处，已实现Online的实现
df_com_online = df_com_online_1.append(df_com_null) 	#Online + 非绑最终结果
df_com_online = df_com_online.reset_index(drop = True)
break_point_5 = timeit.default_timer()
print 'Break point 5 :', break_point_5 - break_point_4
print ' '

#Offline 部分
# 参考：df[(True-df['appID'].isin([278,382]))]  
# 参考：df[(True-df['appID'].isin([278,382]))&(True-df['appPlatform'].isin([2]))]  
# 只除去了976和986，没除去NaN值 df_com_offline_1 = df_com_final[(True - df_com_final['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986']))]
# df_com_offline = df_com_final[(True - df_com_final['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986'])) & (True - df_com_null['Counter Name New'].isnull)]
# 原数-三种情况 df_com_offline = df_com_final[(True - df_com_final['Counter Name New'].isin(df_com_online['Counter Name New']))]	# 相对速度会慢点，类似于SQL的 select in
# df_com_offline = df_com_final_notnull[(True - df_com_final_notnull['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986']))] # 在非空值的基础上去掉976和986，提高运行速度
df_com_offline = df_com_final_notnull[- df_com_final_notnull['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986'])] #上一句存在warning，原因True涉及到布尔值的运算，不能采用'-'运算，网上有其他四种方法
df_com_offline = df_com_offline.reset_index(drop = True)
#以上计算运行时间较长
break_point_6 = timeit.default_timer()
print 'Break point 6 :', break_point_6 - break_point_5
print ' '

def csv_writen_once():
	print 'Length of file' + ' ' + file_flag + ' ' + 'is' + ' ' + str(len(file_pre))
	file_pre.to_csv(path + file_current_name + '\\' + 'Wechat_' + file_flag + '.csv', index = False, encoding = 'utf-8-sig')
	print 'file' + ' ' + file_flag + ' ' + 'has finished!'
	print ' '

def csv_writen_multiple():
	global len_mul_file_confirm_sum
	global n_con
	global second_num_of_times
	len_mul_file_confirm = len(file_pre_s)
	len_mul_file_confirm_sum = len_mul_file_confirm_sum + len_mul_file_confirm
	print '    Length of file_' + str(int(second_num_of_times - n_con)) + ' ' + file_flag + ' ' + 'is' + ' ' + str(len(file_pre_s))
	file_pre_s.to_csv(path + file_current_name + '\\' + 'Wechat_' + file_flag + '_' + str(int(second_num_of_times - n_con)) + '.csv', index = False, encoding = 'utf-8-sig')
	print '    file' + ' ' + '_' + str(int(second_num_of_times - n_con)) + ' ' + file_flag + ' ' + 'has finished!'
	print ' '
	n_con = n_con - 1
	

def end_confirm_once():
	if len(df_com_online) + len(df_com_offline) == len(df_origin):
		print 'Groupby Total Numer is True'
		print ' '
		print 'All filies created. WechatGroupBy has finished!'
		print 'Please transform csv file to excel if nessary.'
	else:
		print 'Something error in processing, please check for it.'

def end_confirm_multiple():
	if len_mul_file_confirm_sum == len(file_pre):
		print '    Split Total Numer is True'
		print ' '
	else:
		print 'Something error in processing split big son file more than 104W, please check for it.'
n = 0
file_flag = 'Online'
len_confirm = len(df_com_online)
file_pre = df_com_online

#file_max_number = 1040000.0
len_confirm_sum = 0
len_mul_file_confirm_sum = 0


#开始写入文件
while n < 2: #Online跑一次，Offline跑一次
	print 'Length of file is:', len_confirm
	file_max_number = round(input('Please input file_max_number: '), 1)
	if len_confirm > file_max_number:
		print 'There exist file more than ' + str(int(file_max_number / 10000)) + 'W, try to split it.'
		print ' '
		#向上取整
		second_num_of_times = len_confirm / file_max_number
		second_num_of_times = math.ceil(second_num_of_times)
		n_con = second_num_of_times
		#对 second_num_of_times 进行循环切片处理
		for y in range(1, int(second_num_of_times)):
			file_pre_s = file_pre[(int(file_max_number) * int(second_num_of_times - n_con)) : (int(file_max_number) * int(second_num_of_times - n_con + 1))]
			csv_writen_multiple()
		file_pre_s = file_pre[(int(file_max_number) * int(second_num_of_times - n_con)) : len(file_pre)]
		csv_writen_multiple()
		end_confirm_multiple()
	else:
		csv_writen_once()
	n = n + 1
	file_flag = 'Offline'
	len_confirm = len(df_com_offline)
	file_pre = df_com_offline
	break_point_7 = timeit.default_timer()
	print 'Break point Round 1 :', break_point_7 - break_point_6
	print ' '

end_confirm_once()