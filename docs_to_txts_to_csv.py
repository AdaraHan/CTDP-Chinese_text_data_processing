"""author: Adara 2023/7/21
需求：
1. 把一个文件夹下所有的.docx文档转化为utf-8的txt文档，然后把所有的txt文档合并成一个文档all_qss.txt
2. 然后对抓取all_qss.txt文本中以“序”结尾的行以及它们的前一行数据，分别写入csv文档中的两列：序名和作者，存储在output.csv中
3. 另外，如果前一行文本字符总数大于10，那么截取前一行文本的前10个字符写入“作者”列
"""
import os
import re
import csv
from docx import Document


def docx_to_txt(file_name, output_file):
    doc = Document(file_name)
    with open(output_file, 'w', encoding='utf-8') as file:
        for para in doc.paragraphs:
            file.write(para.text + '\n')


def combine_txt_files(dir_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(dir_path):
            if filename.endswith('.txt'):
                with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as readfile:
                    outfile.write(readfile.read())


def extract_data(file_name, output_file, delimiter=','):
    # 按行读取文本文件
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 初始化空列表以存储结果
    titles = []
    authors = []

    for i in range(1, len(lines)):
        # 检查当前行是否以"序"结尾
        if lines[i].strip().endswith('引') or lines[i].strip().endswith('叙') or lines[i].strip().endswith('敘'):
            # 如果前一行的字符总数大于10，那么只截取前一行的前10个字符
            previous_line = lines[i - 1].strip()[:10] if len(lines[i - 1].strip()) > 10 else lines[i - 1].strip()
            #  将处理过的前一行存储在titles列表中，将当前行存储在authors列表中
            titles.append(lines[i].strip())
            authors.append(previous_line)

    # 写入csv文件
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(['序名', '作者'])  # 写入表头
        for title, author in zip(titles, authors):
            writer.writerow([title, author])


# # 将docx文件转换为txt
# dir_path = './'  # 文件夹路径
# for filename in os.listdir(dir_path):
#     if filename.endswith('.docx'):
#         docx_to_txt(os.path.join(dir_path, filename), os.path.join(dir_path, filename[:-5] + '.txt'))

# 合并所有的txt文档
# combine_txt_files(dir_path, 'all_qss.txt')

# 对all_qss.txt进行上述正则表达式的全部操作【用修改后的txt文本】
extract_data('all_qss_gai.txt', 'output_yin_xu2.csv', ',')
