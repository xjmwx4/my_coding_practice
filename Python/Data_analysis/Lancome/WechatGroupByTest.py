# -*- coding:utf8 -*-
#

from pandas import DataFrame,Series
import pandas as pd


a = {'A':['USA', 'USA', 'USA', 'CH', 'USA', 'USA', 'F'],
	'B':['Geogle', 'Twitter', 'Facebook', 'Baidu', 'Amazon', 'Apple', 'Dell'],
	'C': [1, -1, 5, 9, -1, 4, 3]
}

b = {'Number':['ChinaLancome976', 'ChinaLancome986', 'ChinaLancome976', 'ChinaLancome986', 'ChinaLancome0P8', 'ChinaLancome986', 'ChinaLancome998', 'ChinaLancome975', 'ChinaLancome0O0', 'ChinaLancome976', 'ChinaLancome986'],
	'Category':['A', 'A', 'B', 'D', 'B', 'D', 'C', 'C', 'B', 'C', 'A'],
	'Date': [1, -1, 5, 9, -1, 4, 3, 4, 9, 2, 8]
}

#初始表的构成
d1 = DataFrame(a, columns = ['A', 'B', 'C'])
d2 = DataFrame(b, columns = ['Number', 'Category', 'Date'])

#d2的处理，目的使选出最大Date下对应的Category，即Lancome的管理柜台定义
d2_1 = d2.sort_values(by = ['Number', 'Date'], ascending = False)
d2_1 = d2_1.reset_index(drop = True)

#d2_1 管理柜台对应表
d2_1 = d2_1.drop_duplicates(['Number'])

#LEFT JOIN，选出其对应的管理柜台，省略不需要用到的列
d3 = pd.merge(d1, d2_1, how = 'left', left_on = 'A', right_on = 'Number')
d3_1 = d3[['A', 'B', 'C', 'Category']]

d3_1_1 = d3_1[d3_1['Category'] == 'ChinaLancome976']
d3_1_2 = d3_1[d3_1['Category'] == 'ChinaLancome854']
d3_1_3 = pd.isnull(d3_1['Category'])
d3_1_4 = d3_1[d3_1_3 == True]


d4 = d3_1_1.append(d3_1_2)
#到此处，已实现Online的实现
d4 = d4.append(d3_1_4)

#Offline的实现

data = pd.read_csv('update.csv', encoding = 'utf-8-sig')

data['Level_Number'] = map(lambda x: 0 if x == 'GC' else x, data['Max_Level_Name']) 								#GC
data['Level_Number'] = map(lambda x: 1 if x == u'\u666e\u901a\u4f1a\u5458' else x, data['Level_Number']) 		#普通会员
data['Level_Number'] = map(lambda x: 2 if x == u'\u94f6\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#银卡会员
data['Level_Number'] = map(lambda x: 3 if x == u'\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 		#金卡会员
data['Level_Number'] = map(lambda x: 4 if x == u'\u9ed1\u91d1\u5361\u4f1a\u5458' else x, data['Level_Number']) 	#黑金卡会员

data = data.sort_values(by = ['Mobile', 'Level_Number', 'Amount of Active Card'], ascending = False)
data = data.drop_duplicates(['Mobile'])
data = data.reset_index(drop = True)


data = pd.read_csv(path + file_current_name + '\OnlineD10.csv', encoding = 'utf-8-sig')
data_11 = pd.read_csv(path + file_current_name + '\data_11.csv', encoding = 'utf-8-sig')
data = data[-data['Mobile Phone'].isin(data_11['Mobile Phone'])]


data_1 = pd.read_csv(path + file_current_name + '\D10before.csv', encoding = 'utf-8-sig')
data_2 = pd.read_csv(path + file_current_name + '\OnlineD10-TMALL-1128.csv', encoding = 'utf-8-sig')

['ChinaLancome890', 'ChinaLancome3I0', 'ChinaLancome3B0', 'ChinaLancome3H0', 'ChinaLancome3M0', 'ChinaLancome3C0', 'ChinaLancome6D0', 'ChinaLancome3K0', 'ChinaLancome3L0', 'ChinaLancome3D0', 'ChinaLancome3E0', 'ChinaLancome3J0', 'ChinaLancome5E0', 'ChinaLancome8J0']