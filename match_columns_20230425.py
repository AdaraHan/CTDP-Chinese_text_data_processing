import pandas as pd
from opencc import OpenCC

# CSV文件路径
input_file = 'souyun_song.csv'
match_file = 'cbdb_qss_isname.csv'
output_file = 'souyun_song_matchqss.csv'


def convert_to_simplified(column):
    cc = OpenCC('t2s')
    return column.apply(lambda x: cc.convert(x))


def main():
    # 读取CSV文件
    csv_A = pd.read_csv(input_file, encoding='utf-8-sig')
    csv_B = pd.read_csv(match_file, encoding='utf-8-sig')

    # 复制列并将繁体转为简体
    csv_A['Author_jian'] = convert_to_simplified(csv_A['Author'])
    csv_A['Title_jian'] = convert_to_simplified(csv_A['Title'])

    csv_B['author_jian'] = convert_to_simplified(csv_B['author'])
    csv_B['title_jian'] = convert_to_simplified(csv_B['title'])

    # 按照简化后的Author和Title列合并两个CSV文件
    merged_data = pd.merge(csv_A, csv_B, left_on=['Author_jian', 'Title_jian'], right_on=['author_jian', 'title_jian'])

    # 从合并后的数据中选择所需列
    result = merged_data[['Id', 'Title', 'Author', 'AuthorId', '#', 'book', 'volume', 'page']]

    # 将结果保存到新的CSV文件
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("处理完成，结果已保存到:", output_file)


if __name__ == "__main__":
    main()
