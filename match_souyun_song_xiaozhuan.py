"""
author:Adara 2023/5/31
"""
import pandas as pd
from opencc import OpenCC

# CSV文件路径
# input_file = 'souyun_song.csv'
# match_file = 'souyun_xiaozhuan.csv'
input_file = 'souyun_xiaozhuan_notmatch_song_process.csv'
match_file = 'CNKGraph.Writings_02_add_cleaned_song.csv'
# output_file = 'souyun_song_match_xiaozhuan.csv'
# output_file_notmatch = 'souyun_song_notmatch_xiaozhuan.csv'
output_file = 'souyun_xiaozhuan_notmatch_song_final.csv'


def convert_to_simplified(column):
    cc = OpenCC('t2s')
    return column.apply(lambda x: cc.convert(x))


def main():
    # 读取CSV文件
    csv_A = pd.read_csv(input_file, encoding='utf-8-sig')
    csv_B = pd.read_csv(match_file, encoding='utf-8-sig')

    # 复制列并将繁体转为简体
    csv_A['Author_jian'] = convert_to_simplified(csv_A['Author_xiaozhuan'])

    csv_B['author_jian'] = convert_to_simplified(csv_B['Author'])

    # =====================【匹配处理】=========================
    # 按照简化后的Author列合并两个CSV文件
    merged_data = pd.merge(csv_A, csv_B, left_on=['Author_jian'], right_on=['author_jian'], how='left', indicator=True)

    # 从合并后的数据中选择所需列
    result = merged_data[
        ['Author_jian', 'AuthorId_xiaozhuan', 'Author_xiaozhuan', 'Xiaozhuan', 'Birthyear', 'Diedyear', 'Rank',
         'Nickname', 'Title', 'Author', 'AuthorId', 'Comments', 'Dynasty']]

    # 将结果保存到新的CSV文件
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("处理完成，结果已保存到:", output_file)

    # # =================【不匹配处理】=======================
    # # 根据AuthorId和Id列进行匹配，采用外连接
    # merged_data = pd.merge(csv_A, csv_B, left_on=['AuthorId'], right_on=['AuthorId'], how='outer', indicator=True)
    #
    # # 选择与标签为“left_only”的行，即不匹配的数据
    # unmatched_data = merged_data.loc[merged_data['_merge'].isin(['left_only'])]
    # # unmatched_data = merged_data.loc[merged_data['_merge'].isin(['right_only'])]
    #
    # # 删除合并指示符列
    # unmatched_data = unmatched_data.drop(columns=['_merge'])
    #
    # # 从合并后的数据中选择所需列
    # # result = unmatched_data[['Id', 'Author', 'AuthorId']]
    # # result = unmatched_data.reindex(columns=['Id', 'Title', 'Author', 'AuthorId'])
    # result = unmatched_data.reindex(
    #     columns=['AuthorId', 'Author', 'Xiaozhuan', 'Birthyear', 'Diedyear', 'Rank', 'Nickname'])
    #
    # # 将不匹配的数据保存到新的CSV文件
    # result.to_csv(output_file_notmatch, index=False, encoding='utf-8-sig')
    # print("【不匹配】处理完成，结果已保存到:", output_file_notmatch)


if __name__ == "__main__":
    main()
