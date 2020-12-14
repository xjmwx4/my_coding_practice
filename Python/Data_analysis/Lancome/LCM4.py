# -*- coding:utf8 -*-
# author：Fitz.Xu
# file function: Lifecycle M4

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import random
import math

#设置文件读取路径，直接从文件目录读取，注意转义问题
path = 'D:\Otype-Fitz.Xu\Lorealparis\Lancome\\1RegularSMS\\'
file_current_name = str(input('Please input current file date (yyyyMMDD): '))

data = pd.read_csv(path + file_current_name + '\LCM4.csv', sep = '\t' , encoding = 'utf-16')
data = data[data['Points'] >= 200]
data = data.reset_index(drop = True)
data = data.sort_values(by = ['Mobile Phone', 'Points'], ascending = False)
data = data.drop_duplicates(['Mobile Phone'])
#data = data.sort_values(by = 'Mobile Phone', ascending = True)
data = data.reset_index(drop=True)

file_date = str(input('Enter File Date: '))

data['id'] = random.sample(range(len(data.index)), len(data.index))
con_flag_data = data['id']
con_flag_data = sorted(con_flag_data)
#Control组设置
data['Control Group'] = map(lambda x: 'Control' if x>=con_flag_data[len(con_flag_data) - len(con_flag_data) / 10 ] else 'Sending', data['id'])
#设置文件写入路径，直接从文件目录写入，注意转义问题即要加 '\\' 这部分
data.to_csv(path + file_current_name + '\\' + 'Lifecycle-M4-1' + file_date + '.csv', index = False, encoding = 'utf-8-sig')
print ''
print 'Lifecycle-M4-' + file_date + ' ' + 'has finished!'