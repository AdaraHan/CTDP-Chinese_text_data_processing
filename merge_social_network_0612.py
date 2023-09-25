"""author:Adara 2023/6/12
需求：合并后的新表匹配CBDB的SNA关系，并计算匹配到的人名次数
"""
import pandas as pd

# 读取csv文件
df_A = pd.read_csv('test_merged_rengong_cbdbid_0612.csv', encoding='utf-8-sig')
df_B = pd.read_csv('test_social_network_song_0612.csv', encoding='utf-8-sig')

# 不考虑顺序，比较A文档中的姓名两列是否在B文档中的姓名两列中
df_A['social_network_Author'] = df_A.apply(
    lambda row: 'is' if set([row['Author'], row['name_in_title']]) in df_B[['姓名', '社會關係人姓名']].apply(set,
                                                                                                             axis=1).tolist() else 'no',
    axis=1)

# 标题姓名列中每个名字匹配到 'is' 的次数
df_is = df_A[df_A['social_network_Author'] == 'is']
count_is = df_is.groupby('name_in_title').size()
df_A['times_name'] = df_A['name_in_title'].map(count_is)

# 保存为csv文件
df_A.to_csv('test_output.csv', index=False, encoding='utf-8-sig')
