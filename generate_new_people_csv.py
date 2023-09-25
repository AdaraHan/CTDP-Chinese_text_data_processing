"""author:Adara 2023.08.14
需求：提取latest表中count值为1、2且decision值为"0-n或n或n_wh或null或y-n"的数据，并去除这些数据中对应的人名与剩余人名相同的数据。
备注：__y或_y或0-y或n_wh-y或n-y或y或y_wh
思路：
1. 首先，加载csv文件到pandas的DataFrame。
2. 根据条件筛选出第一组数据。
3. 筛选出不在第一组中的数据为第二组。
4. 从第一组中删除那些其AuthorId_rengong列值也在第二组中的数据。
5. 将结果保存到新的csv文件。
"""
import pandas as pd

# 1. 加载csv文件
df = pd.read_csv('merged_rengong_cbdbid_latest.csv', 'r', encoding='UTF-8', delimiter=',')
print(df.columns)
print(df.head)

# 2. 根据条件筛选出第一组数据
condition_1 = df[(df['count'].isin([None, 1, 2])) & (df['decision'].isin(['0-n', 'n', 'n_wh', 'null', 'y-n']))]

# 3. 筛选出不在第一组中的数据为第二组
condition_2_ids = df[~df.index.isin(condition_1.index) & (df['count'] >= 3) | (
    df['decision'].isin(['__y', '_y', '0-y', 'n_wh-y', 'n-y', 'y', 'y_wh']))]['AuthorId_rengong']

# 4. 从第一组中删除那些其AuthorId_rengong列值也在第二组中的数据
result = condition_1[~condition_1['AuthorId_rengong'].isin(condition_2_ids)]

# 5. 保存到新的csv文件
result.to_csv('new_people_to_cbdb.csv', index=False, encoding='utf-8-sig')
