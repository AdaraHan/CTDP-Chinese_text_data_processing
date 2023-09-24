"""author: Adara 2023/4/10
需求：清理csv数据格式
代码思路：
1. 读取csv文件
2. 清理数据【正则提取相关信息，只保存了content里的第一条内容（title和clause）】
3. 保存数据
"""
import pandas as pd
import json
import re

input_file = "CNKGraph.Writings_02.csv"
output_file = "CNKGraph.Writings_02_cleaned.csv"


# 定义一个函数来提取单元格中的文本
def extract_text(cell):
    if not isinstance(cell, str):
        return cell

    # content_pattern = re.compile(r"'Content':\s*'([^']+)'\s*(?:,\s*'Comments')")  # 只清理含'Comments'的数据
    content_pattern = re.compile(r"'Content':\s*'([^']+)'\s*(?:,\s*'Comments')?")
    match = content_pattern.search(cell)
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

    if cell.__contains__("'Content'"):
        try:
            content_matches = match.group(1)
            cell = "".join(content_matches)
        except:
            pass
    elif cell.startswith("["):
        try:
            chinese_matches = chinese_pattern.findall(cell)
            cell = "".join(chinese_matches)
        except json.JSONDecodeError:
            pass

    # 进一步清理非数组或对象的JSON格式内容
    cell = re.sub(r'〖', '', cell)
    cell = re.sub(r'〗', '', cell)

    return cell


# 读取CSV数据
df = pd.read_csv(input_file, sep=",", encoding="utf-8-sig", low_memory=False)  # low_memory=False 防止警告

# 清理数据
df = df.applymap(extract_text)  # 对每个单元格应用提取文本的函数

# 保存清理后的数据到新的CSV文件
df.to_csv(output_file, index=False, sep=",", encoding="utf-8-sig")

print("\n数据已清理并保存到新的CSV文件")
