import pandas as pd

input_file = 'output20190214_isname.csv'
output_file = 'output20190214_isname_quchong.csv'

# 去重
# 读取CSV文件
df = pd.read_csv(input_file, encoding='utf-8-sig')
# 整行去重
# df_unique = df.drop_duplicates()
# 根据指定列去除重复行
column_name = ['AuthorId']
df_unique = df.drop_duplicates(subset=column_name)

# 将去重后的数据写入输出文件
df_unique.to_csv(output_file, index=False, encoding='utf-8-sig')

print("【去重】处理完成，结果已保存到:", output_file)
