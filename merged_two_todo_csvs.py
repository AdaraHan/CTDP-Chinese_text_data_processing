import pandas as pd

# 读取A和C两个CSV文件
a_df = pd.read_csv('todo_merged_rengong_cbdbid_latest.csv')
c_df = pd.read_csv('todo_matched_people_cbdbid_proofreaded.csv')

# 使用pandas的merge功能按照“AuthorId_rengong”字段进行左连接
merged_df = a_df.merge(c_df[['AuthorId_rengong', 'xiaozhuan_x']], on='AuthorId_rengong', how='left',
                       suffixes=('', '_from_C'))

# 使用numpy的where方法来更新“xiaozhuan_x”字段
merged_df['xiaozhuan_x'] = merged_df['xiaozhuan_x'].where(merged_df['xiaozhuan_x_from_C'].isnull(),
                                                          merged_df['xiaozhuan_x_from_C'])

# 删除不必要的辅助列
merged_df.drop(columns=['xiaozhuan_x_from_C'], inplace=True)

# 将结果保存回A文件或新的CSV文件
merged_df.to_csv('Updated_merged_rengong_cbdbid_latest.csv', index=False, encoding='utf-8-sig')

