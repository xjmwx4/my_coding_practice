
data_or_0 = pd.read_csv('bycounter.csv', encoding = 'utf-8-sig')
data_p = pd.read_csv('LIST.csv', encoding = 'utf-8-sig')
data_com = pd.merge(data_or_0, data_p, how='left', left_on = ['Contact or Prospect ID', 'ROW_ID'], right_on = ['cp_id','ROW_ID'])
data_com.index
data_com.to_csv('MM.csv',index=False,encoding='utf-8-sig')
data_or = data_com

data_or = pd.read_csv('MM.csv', encoding = 'utf-8-sig')

data_mars = pd.read_csv('Mars.csv',encoding = 'utf-8-sig')

data_com_step1 = pd.merge(data_or, data_mars, how = 'left', left_on = 'Counter Name New', right_on = 'MARS')

data_com_step1['Convert_to_TF1'] = map(lambda x: True if pd.isnull(x) == True else False, data_com_step1['Convert_to'])

data_com_step1['Convert_to_TF1'] = map(lambda x: data_com_step1['Counter Name New'] if x == True else data_com_step1['Convert_to'], data_com_step1['Convert_to_TF1'])

