# -*- coding:utf8 -*-
from pandas import Series, DataFrame
import pandas as pd
import random

data = pd.read_csv('OnlineDailyBirthday.csv')

#Control组设置部分
data['id'] = random.sample(range(10000), len(data.index))
con_flag = data['id']
con_flag = sorted(con_flag)
data['Control Group'] = map(lambda x: 'Control' if x>=con_flag[len(con_flag) - len(con_flag) / 10 ] else 'Sending', data['id'])

filename = "OnlineDailyBirthday-1101.csv"

data.to_csv(filename, index = False)


def csv_to_xlsx_pd():
    csv = pd.read_csv(filename, encoding='GB2312')
    csv.to_excel('OnlineDailyBirthday-1101.xlsx', sheet_name='OnlineDailyBirthday-1101', index = False)


if __name__ == '__main__':
    csv_to_xlsx_pd()
