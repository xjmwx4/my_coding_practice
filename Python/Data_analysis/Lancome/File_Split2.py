# -*- coding:utf8 -*-
#

from pandas import DataFrame, Series
import pandas as pd
import math #涉及到除法向上取整的问题

file_or = pd.read_csv('ETL1711W201_New2.csv')

#列名的选取 
a_1 = file_or.columns.values #array, b = { 'Y': a}, c= DataFrame(b)
a_2 = {'C_Name': a_1}
a_3 = DataFrame(a_2)

b_1 = file_or[file_or.index == 0].values
b_2 = b_1.T
b_3 = DataFrame(b_2)

a_3['R0_Name'] = b_3

print a_3
print ' '

#
columns_flag = input('Confirm Column name. Please Input the Column Name:')
print ' '

# a_3['Y'][columns_flag] 为需要选取的列名称
columns_final_name = a_3['C_Name'][columns_flag]
#file_or[columns_final_name].head()

#查看所选列unique值，并对其进行重新index便于之后选取
d_1 = file_or[columns_final_name].unique()
d_2 = {'Unique_Values': d_1}
d_3 = DataFrame(d_2)

print 'Unique Values:'
print d_3
print ' '

#去重后的值，可看到index和所选列名的所有情况
#file_or.drop_duplicates([columns_final_name])

len_confirm = 0
len_confirm_sum = 0
len_mul_file_confirm = 0
len_mul_file_confirm_sum = 0

def csv_writen_once():
	print 'Length of file' + ' ' + d_3['Unique_Values'][x] + ' ' + 'is' + ' ' + str(len(file_pre))
	file_pre.to_csv(d_3['Unique_Values'][x] + '.csv', index = False, encoding = 'utf-8-sig')
	print 'file' + ' ' + str(x+1) + ' ' + d_3['Unique_Values'][x] + ' ' + 'has finished!'
	print ' '

def csv_writen_multiple():
	global len_mul_file_confirm_sum
	global n_con
	global second_num_of_times
	len_mul_file_confirm = len(file_pre_s)
	len_mul_file_confirm_sum = len_mul_file_confirm_sum + len_mul_file_confirm
	print '    Length of file_' + str(int(second_num_of_times - n_con)) + ' ' + d_3['Unique_Values'][x] + ' ' + 'is' + ' ' + str(len(file_pre_s))
	file_pre_s.to_csv(d_3['Unique_Values'][x] + '_' + str(int(second_num_of_times - n_con)) + '.csv', index = False, encoding = 'utf-8-sig')
	print '    file' + ' ' + str(x+1) + '_' + str(int(second_num_of_times - n_con)) + ' ' + d_3['Unique_Values'][x] + ' ' + 'has finished!'
	print ' '
	n_con = n_con - 1
	

def end_confirm_once():
	if len_confirm_sum == len(file_or):
		print 'Split Total Numer is True'
		print ' '
		print 'All filies created. File split has finished!'
		print 'Please transform csv file to excel if nessary.'
	else:
		print 'Something error in processing, please check for it.'

def end_confirm_multiple():
	if len_mul_file_confirm_sum == len(file_pre):
		print '    Split Total Numer is True'
		print ' '
	else:
		print 'Something error in processing split big son file more than 104W, please check for it.'

#循环部分
for x in range(0, len(d_3)):
	print 'Processing......'
	file_pre = file_or[file_or[columns_final_name] == d_3['Unique_Values'][x]]
	file_pre = file_pre.reset_index(drop=True)
	#len_confirm_sum = len_confirm
	len_confirm = len(file_pre)
	len_confirm_sum = len_confirm_sum + len_confirm

	file_max_number = 1040000.0
	#当拆分行数大于104W行时，对其进行二次分割
	if len_confirm > file_max_number:
		print 'There exist file more than 104W, try to split again.'
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
		
end_confirm_once()


