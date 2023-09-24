"""author: Adara 2023/4/24
需求：output20190214_isname_update_match_xiaozhuan_notmatch.csv与CNKGraph.Writings_02_add_cleaned_song.csv匹配
得到最终的author_notmatch.csv
发现：有重复数据，需要去重
解决：使用pandas的drop_duplicates()方法去重
"""
import pandas as pd
from opencc import OpenCC

# CSV文件路径
input_file = 'output20190214.csv'
match_file = 'CNKGraph.Writings_02_add_cleaned_song_quchong.csv'
output_file = 'output20190214_author_notmatch.csv'
quchong_file = 'output20190214_author_notmatch_quchong.csv'


def convert_to_simplified(column):
    cc = OpenCC('t2s')
    return column.apply(lambda x: cc.convert(x))


def main():
    # 读取CSV文件
    csv_A = pd.read_csv(input_file, encoding='utf-8-sig')
    csv_B = pd.read_csv(match_file, encoding='utf-8-sig')

    # 复制列并将繁体转为简体
    csv_A['author_jian'] = convert_to_simplified(csv_A['author'])
    csv_B['Author_jian'] = convert_to_simplified(csv_B['Author'])
    field_to_compare_file1 = 'author_jian'
    field_to_compare_file2 = 'Author_jian'

    # 找到第一个csv文件中与第二个csv文件中不匹配的数据
    merged_df = csv_A.merge(csv_B, left_on=field_to_compare_file1, right_on=field_to_compare_file2, how='left',
                            indicator=True)
    result_df = merged_df[merged_df['_merge'] == 'left_only']
    # 删除多余的列
    result_df = result_df.drop(columns=[field_to_compare_file2, '_merge'])

    # 将结果保存到新的CSV文件
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("【不匹配】处理完成，结果已保存到:", output_file)


if __name__ == "__main__":
    main()

# 去重
# 读取CSV文件
df = pd.read_csv(output_file, encoding='utf-8-sig')
# 整行去重
# df_unique = df.drop_duplicates()
# 根据指定列去除重复行
column_name = ['author-id']
df_unique = df.drop_duplicates(subset=column_name)

# 将去重后的数据写入输出文件
df_unique.to_csv(quchong_file, index=False, encoding='utf-8-sig')

print("【去重】处理完成，结果已保存到:", quchong_file)
