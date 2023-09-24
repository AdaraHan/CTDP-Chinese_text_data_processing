"""author: Adara 2023/4/17
需求：上一步得到的表output20190214_isname_update_match.csv与搜韵《全宋诗作者小传》匹配，输出匹配和不匹配的两个文档
遇到问题：KeyError: "['Id'] not in index"
原因排查：input_file文档也有“Id”列，与match_file文档的“Id”列重名
解决方案：将input_file文档的“Id”列删除
"""
import pandas as pd

# CSV文件路径
input_file = 'output20190214_isname_update_match.csv'
match_file = '全宋诗作者小传.csv'
output_file1 = 'output20190214_isname_update_match_xiaozhuan.csv'
output_file2 = 'output20190214_isname_update_match_xiaozhuan_notmatch.csv'
output_file3 = '全宋诗作者小传_notmatch.csv'
quchong_file = 'output20190214_isname_update_match_xiaozhuan_notmatch_quchong.csv'


def main():
    # 读取CSV文件
    csv_A = pd.read_csv(input_file, sep=',', encoding='utf-8-sig')
    csv_B = pd.read_csv(match_file, sep=',', encoding='utf-8-sig')

    # 检查列名是否存在
    if 'AuthorId' in csv_A.columns and 'Id' in csv_B.columns:
        print("列名匹配")
        # 输出列名
        print("A.csv columns:", csv_A.columns)
        print("B.csv columns:", csv_B.columns)
    else:
        print("列名不匹配")

    # 【匹配处理】
    # 根据AuthorId和Id列进行匹配
    merged_data = pd.merge(csv_A, csv_B, left_on='AuthorId', right_on='Id')

    # 从合并后的数据中选择所需列
    result = merged_data[
        ['author-id', 'author', 'title', 'line_id', 'book', 'volume', 'page',
         'Id', '姓名', '小传', '生年', '卒年', '行第', '各类别称']]

    # 将结果保存到新的CSV文件
    result.to_csv(output_file1, index=False, encoding='utf-8-sig')
    print("【匹配】处理完成，结果已保存到:", output_file1)

    # 【不匹配处理】
    # 根据AuthorId和Id列进行匹配，采用外连接
    merged_data = pd.merge(csv_A, csv_B, left_on='AuthorId', right_on='Id', how='outer', indicator=True)

    # 选择与标签为“left_only”的行，即不匹配的数据
    unmatched_data1 = merged_data.loc[merged_data['_merge'].isin(['left_only'])]
    unmatched_data2 = merged_data.loc[merged_data['_merge'].isin(['right_only'])]

    # 删除合并指示符列
    unmatched_data1 = unmatched_data1.drop(columns=['_merge'])
    unmatched_data2 = unmatched_data2.drop(columns=['_merge'])

    # 从合并后的数据中选择所需列
    result1 = unmatched_data1[['author-id', 'author', 'title', 'line_id', 'book', 'volume', 'page']]
    result2 = unmatched_data2[['Id', '姓名', '小传', '生年', '卒年', '行第', '各类别称']]

    # 将不匹配的数据保存到新的CSV文件
    result1.to_csv(output_file2, index=False, encoding='utf-8-sig')
    result2.to_csv(output_file3, index=False, encoding='utf-8-sig')
    print("【不匹配】处理完成，结果已保存到:", output_file2, output_file3)


if __name__ == "__main__":
    main()

# 去重
# 读取CSV文件
df = pd.read_csv(output_file2, encoding='utf-8-sig')
# 整行去重
# df_unique = df.drop_duplicates()
# 根据指定列去除重复行
column_name = ['author-id']
df_unique = df.drop_duplicates(subset=column_name)

# 将去重后的数据写入输出文件
df_unique.to_csv(quchong_file, index=False, encoding='utf-8-sig')

print("【去重】处理完成，结果已保存到:", quchong_file)
