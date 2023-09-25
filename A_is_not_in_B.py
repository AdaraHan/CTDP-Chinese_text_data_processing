import pandas as pd

# 读取两个CSV文件
a_df = pd.read_csv('Updated_merged_rengong_cbdbid_latest.csv')
b_df = pd.read_csv('finished_new_people_to_cbdb.csv')

# 获取B文件中“AuthorId_rengong”的所有唯一值
b_ids = set(b_df['AuthorId_rengong'].unique())

# 筛选A文件中不包含B文件“AuthorId_rengong”的所有数据
result = a_df[~a_df['AuthorId_rengong'].isin(b_ids)]

# 如果需要，可以保存结果到新的CSV文件
result.to_csv('result_Updated_merged_rengong_cbdbid_latest.csv', index=False, encoding='utf-8-sig')
