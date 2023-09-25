"""
需求：过滤CNKGraph.Writings_02_add_cleaned_song.csv和output20190214_isname.csv中的列
"""
import pandas as pd

input_file = "CNKGraph.Writings_02_add_cleaned_song.csv"
output_file = "souyun_song.csv"
# 定义要保留的列名列表
columns_to_keep = ["Id", "Title", "Author", "AuthorId"]

# input_file = "output20190214_isname.csv"
# output_file = "cbdb_qss_isname.csv"
# # 定义要保留的列名列表
# columns_to_keep = ["#", "book", "volume", "page", "author", "title"]


def filter_columns(input_file, output_file, columns_to_keep):
    # 读取CSV文件
    data = pd.read_csv(input_file, encoding="utf-8-sig")

    # 保留指定的列
    filtered_data = data[columns_to_keep]

    # 将筛选后的数据保存到新的CSV文件中
    filtered_data.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"【过滤列】已被保存到新文件 {output_file}.")


filter_columns(input_file, output_file, columns_to_keep)
