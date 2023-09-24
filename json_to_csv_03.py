"""author: Adara 2023/4/11
需求：【清理csv数据格式】对上一步清理完的csv数据增加一列，存储原始的诗歌内容，以便后续训练模型
代码思路：
1. 直接复制一列数据
2. 保存数据
3. 读取保存后数据
4. 处理保存后的数据
"""
import pandas as pd
import json
import re

# 读取CSV文件
input_file = "CNKGraph.Writings_02.csv"
output_file = "CNKGraph.Writings_02_add.csv"
cleaned_file = "CNKGraph.Writings_02_add_cleaned.csv"

df1 = pd.read_csv(input_file, sep=",", encoding="utf-8-sig", low_memory=False)

# 创建新列"OriginalClauses"，并复制"Clause"列的数据
df1['OriginalClauses'] = df1['Clauses']

# 保存更改后的CSV文件
df1.to_csv(output_file, index=False, sep=",", encoding="utf-8-sig")

print(df1.columns)  # 查看列名，用于后续指定要保留的列


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


# 读取 添加完新列的CSV 文件
df2 = pd.read_csv(output_file, sep=",", encoding="utf-8-sig", low_memory=False)

# 备份想跳过的列
skipped_column = df2['OriginalClauses'].copy()

# 指定要保留的列
columns_to_use = ['GroupIndex', 'Pictures', 'Id', 'Title', 'Author', 'AuthorId',
                  'Comments', 'Allusions', 'SubTitle', 'AuthorDate', 'TuneId', 'Froms',
                  'TypeDetail', 'AuthorPlace', 'Classes', 'Rhyme', 'Preface', 'Dynasty',
                  'Type', 'Clauses', 'Note']

# 读取 CSV 文件，只使用指定的列
df2 = pd.read_csv(output_file, usecols=columns_to_use, sep=",", encoding="utf-8-sig", low_memory=False)

# 清理数据
df2 = df2.applymap(extract_text)  # 对每个单元格应用提取文本的函数

# 将跳过的列添加回处理后的 DataFrame
df2['OriginalClauses'] = skipped_column

# 保存更改后的CSV文件
df2.to_csv(cleaned_file, index=False, sep=",", encoding="utf-8-sig")

print("\n数据已清理并保存到新的CSV文件")
