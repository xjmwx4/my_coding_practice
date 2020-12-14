
from pandas import Series, DataFrame
import pandas as pd
import random
import csv
import xlwt

data = pd.read_csv('OnlineDailyBirthday_sig.csv', encoding = 'utf-8-sig')

#data['Birthday'] = pd.to_datetime(data['Birthday'])

#Control组设置部分
data['id'] = random.sample(range(10000), len(data.index))
con_flag = data['id']
con_flag = sorted(con_flag)
data['Control Group'] = map(lambda x: 'Control' if x>=con_flag[len(con_flag) - len(con_flag) / 10 ] else 'Sending', data['id'])

filename = "OnlineDailyBirthday_sig-1101"

data.to_csv(filename + '.csv', index = False, encoding = 'utf-8-sig')


