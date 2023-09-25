"""author: Adara 2023/4/24
需求：《全宋诗》人名内部消歧
思路：
1.  读取output20190214.csv原始表，与output-author.csv匹配，将author-id更新到原始表中
2.  更新后的output20190214.csv表与全宋诗重名人物.csv匹配，将重名人物的author-id后添加小数点
"""

import pandas as pd
import opencc

input_file = 'souyun_song_matchqss_quchong_mergedxiaozhuan.csv'
# match_file1 = 'output-author.csv'
match_file2 = '全宋诗重名人物.csv'
output_file1 = 'souyun_song_matchqss_quchong_mergedxiaozhuan_xiaoqi.csv'
# output_file2 = 'output20190214_id_updated.csv'


# # 更新author-id
# def update_author_ids(file_A, file_B, output_file):
#     # 读取两个CSV文件
#     df_A = pd.read_csv(file_A, encoding='utf-8-sig')
#     df_B = pd.read_csv(file_B, encoding='utf-8-sig')
#
#     # 将B文件的author列设为索引，以便后续使用
#     df_B = df_B.set_index('author')
#
#     # 更新A文件中的author-id
#     for index, row in df_A.iterrows():
#         author = row['author']
#         if author in df_B.index:
#             df_A.at[index, 'author-id'] = df_B.at[author, 'author-id']
#
#     # 输出结果
#     df_A.to_csv(output_file, index=False, encoding='utf-8-sig')
#     print("【author-id更新】处理完成，结果已保存到:", output_file)
#
#
# update_author_ids(input_file, match_file1, output_file1)

# 创建繁体转简体的转换器
converter = opencc.OpenCC('t2s.json')

# 读取A文档数据
a_df = pd.read_csv(input_file, encoding='utf-8-sig')

# 读取B文档数据
b_df = pd.read_csv(match_file2, encoding='utf-8-sig')

# 将A文档的Author列转换为简体中文
a_df['Author_jian'] = a_df['Author_x'].apply(converter.convert)

# 找到简体中文名字相同行，并在对应的id列后添加小数点
a_df.loc[a_df['Author_jian'].isin(b_df['name']), 'AuthorId'] = a_df['AuthorId'].astype(str) + '.1'

# 删除临时列（简体作者名）
a_df.drop(columns=['Author_jian'], inplace=True)

# 将更新后的A文档数据写回到文件
a_df.to_csv(output_file1, index=False, encoding='utf-8-sig')

print('【内部消歧】更新完成，结果已保存。')
