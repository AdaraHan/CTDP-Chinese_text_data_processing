"""author: Adara 2023/4/14
需求：在原始的output20190214表中剔除非姓名的数据（姓名字符数大于4，或者小于等于3的里面包含特殊称谓）
遇到问题：一开始用author_id去重，但是发现有些author清理不彻底，所以改用author去重【发现output20190214存在一个id对应多个作者】
解决方法：输出文档按照author列与原始output-author文档重新匹配author_id
"""
import pandas as pd

# CSV文件路径
file_A = 'output20190214.csv'
file_B = 'output_newpeople_character_over4.csv'
file_C = 'output_newpeople_character3_notname.csv'
output_file1 = 'output20190214_isname.csv'
match_file = 'output-author.csv'
output_file2 = 'output20190214_isname_update.csv'


def remove_rows_with_common_author_id(file_A, file_B, file_C, output_file1):
    # 读取三个CSV文件
    df_A = pd.read_csv(file_A, encoding='utf-8-sig')
    df_B = pd.read_csv(file_B, encoding='utf-8-sig')
    df_C = pd.read_csv(file_C, encoding='utf-8-sig')

    # 获取B和C文档中的author集合
    authors_B = set(df_B['author'])
    authors_C = set(df_C['author'])

    # 筛选A文档中不在B和C文档中的author对应的行
    filtered_df_A = df_A[~df_A['author'].isin(authors_B | authors_C)]

    # 输出结果
    filtered_df_A.to_csv(output_file1, index=False, encoding='utf-8-sig')
    print("处理完成，结果已保存到:", output_file1)


def update_author_ids(file_A, file_B, output_file2):
    # 读取两个CSV文件
    df_A = pd.read_csv(file_A, encoding='utf-8-sig')
    df_B = pd.read_csv(file_B, encoding='utf-8-sig')

    # 将B文件的author列设为索引，以便后续使用
    df_B = df_B.set_index('author')

    # 更新A文件中的author-id
    for index, row in df_A.iterrows():
        author = row['author']
        if author in df_B.index:
            df_A.at[index, 'author-id'] = df_B.at[author, 'author-id']

    # 输出结果
    df_A.to_csv(output_file2, index=False, encoding='utf-8-sig')
    print("处理完成，结果已保存到:", output_file2)


remove_rows_with_common_author_id(file_A, file_B, file_C, output_file1)
update_author_ids(output_file1, match_file, output_file2)
