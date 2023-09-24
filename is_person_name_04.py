"""author: Adara 2023/4/17
需求：
上一步得到的表格output20190214_isname_update.csv的author、title列简化后结果
与搜韵的Author、Title列简化后的结果进行匹配
得到最终的output20190214_isname_update_match.csv
"""
import pandas as pd
from opencc import OpenCC

# CSV文件路径
input_file = 'output20190214_isname_update.csv'
match_file = 'CNKGraph.Writings_02_add_cleaned_song.csv'
output_file = 'output20190214_isname_update_match.csv'


# output_file1 = 'output20190214_isname_update_match_AuthorOnly.csv'
# output_file2 = 'output20190214_isname_update_nomatchAuthorOnly.csv'


def convert_to_simplified(column):
    cc = OpenCC('t2s')
    return column.apply(lambda x: cc.convert(x))


def main():
    # 读取CSV文件
    csv_A = pd.read_csv(input_file, encoding='utf-8-sig')
    csv_B = pd.read_csv(match_file, encoding='utf-8-sig')

    # 复制列并将繁体转为简体
    csv_A['author_jian'] = convert_to_simplified(csv_A['author'])
    csv_A['title_jian'] = convert_to_simplified(csv_A['title'])

    csv_B['Author_jian'] = convert_to_simplified(csv_B['Author'])
    csv_B['Title_jian'] = convert_to_simplified(csv_B['Title'])

    # 按照简化后的Author和Title列合并两个CSV文件
    merged_data = pd.merge(csv_A, csv_B, left_on=['author_jian', 'title_jian'], right_on=['Author_jian', 'Title_jian'])
    # merged_data1 = pd.merge(csv_A, csv_B, left_on=['author_jian'], right_on=['Author_jian'])
    # merged_data2 = pd.merge(csv_A, csv_B, left_on=['title_jian'], right_on=['Title_jian'])

    # 从合并后的数据中选择所需列
    result = merged_data[
        ['author-id', 'author', 'title', 'line_id', 'book', 'volume', 'page',
         'AuthorId', 'Author', 'Title', 'Dynasty', 'Clauses',
         'author_jian', 'title_jian', 'Author_jian', 'Title_jian']]  # 注意：这里不用Id列，因为下面要处理的文档Id与这里的Id不同

    # 将结果保存到新的CSV文件
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("处理完成，结果已保存到:", output_file)


if __name__ == "__main__":
    main()
