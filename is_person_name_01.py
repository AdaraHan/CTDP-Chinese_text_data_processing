"""author: Adara 2023/4/3
需求：输出output-newpeople表【CBDB中没有的人物】中人名绝对错误的数据
思路：
1. 筛选姓名列（author）中中文字符总数大于4的数据
2. 输出姓名列（author）中中文字符总数小于4的数据，观察数据，以作进一步处理。
3. 筛选output-newpeople.xls表姓名列（author）中文字符总数小于4的数据里，包含称谓、官职的数据。
"""
import pandas as pd

input_file = "output-newpeople.xls"
# output_file = "output_newpeople_character_over4.xls"
output_file = "output_newpeople_character3.xls"

# 读取Excel文件
df = pd.read_excel(input_file)

# 选择需要筛选的列
col_name = "author"

# 筛选出中文字符数大于等于4的数据
# df_filtered = df[df[col_name].str.count('[\u4e00-\u9fa5]') >= 4]
df_filtered = df[df[col_name].str.count('[\u4e00-\u9fa5]') < 4]

# 将筛选结果保存为Excel文件
writer = pd.ExcelWriter(output_file)
df_filtered.to_excel(writer, index=False)
writer.save()

print("处理完成，结果已保存到:", output_file)
