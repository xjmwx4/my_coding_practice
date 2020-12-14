# -*- conding:utf8 -*-


from pandas import DataFrame,Series
import pandas as pd
import math


#基本思路，先对微信匹配表进行by openid by date排序，重置下index，然后by openid 去重，留下index最小的值
df_origin = pd.read_csv('ms_member20171110.csv', sep = '\t', encoding = 'utf-16')
df_wechat_com = pd.read_csv('WechatCom_test.csv', sep = '\t', encoding = 'utf-16')

df_wechat_com_sort = df_wechat_com.sort_values(by = ['Social Network ID', 'Last Transaction Date(Sale Order)'], ascending = False)
df_wechat_com_sort = df_wechat_com_sort.reset_index(drop = True)
df_wechat_com_sort = df_wechat_com_sort.drop_duplicates(['Social Network ID'])
df_wechat_com_sort = df_wechat_com_sort.reset_index(drop = True)

#LEFT JOIN后结果，一一对应表
df_com = pd.merge(df_origin, df_wechat_com_sort, how = 'left', left_on = 'openid', right_on = 'Social Network ID')
df_com_final = df_com[['membersid', 'mobile', 'openid', 'marsid', 'Counter Name New']]
df_com_final_notnull = df_com_final[df_com_final['Counter Name New'].notnull()] 	# 新建一个非空值的表，用于之后使用

#Online+非绑会员
df_com_TMALL = df_com_final[df_com_final['Counter Name New'] == 'ChinaLancome976']
df_com_EC = df_com_final[df_com_final['Counter Name New'] == 'ChinaLancome986']
df_com_null_0 = pd.isnull(df_com_final['Counter Name New'])
df_com_null = df_com_final[df_com_null_0 == True]

#Online部分
df_com_online_1 = df_com_TMALL.append(df_com_EC)
#到此处，已实现Online的实现
df_com_online = df_com_online_1.append(df_com_null) 	#Online + 非绑最终结果
df_com_online = df_com_online.reset_index(drop = True)

#Offline 部分
# 参考：df[(True-df['appID'].isin([278,382]))]  
# 参考：df[(True-df['appID'].isin([278,382]))&(True-df['appPlatform'].isin([2]))]  
# 只除去了976和986，没除去NaN值 df_com_offline_1 = df_com_final[(True - df_com_final['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986']))]
# df_com_offline = df_com_final[(True - df_com_final['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986'])) & (True - df_com_null['Counter Name New'].isnull)]
# 原数-三种情况 df_com_offline = df_com_final[(True - df_com_final['Counter Name New'].isin(df_com_online['Counter Name New']))]	# 相对速度会慢点，类似于SQL的 select in
df_com_offline = df_com_final_notnull[(True - df_com_final_notnull['Counter Name New'].isin(['ChinaLancome976', 'ChinaLancome986']))] # 在非空值的基础上去掉976和986，提高运行速度
df_com_offline = df_com_offline.reset_index(drop = True)


