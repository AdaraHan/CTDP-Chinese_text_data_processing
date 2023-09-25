"""
需求：匹配两个有关系的人名是否在CBDB社会关系中出现
"""
import pandas as pd

# 加载CSV文件
csv_file_path1 = "社会关系_output.csv"
csv_file_path2 = "social_network_song.csv"

# 读取两个CSV文件
data1 = pd.read_csv(csv_file_path1)
data2 = pd.read_csv(csv_file_path2)

# 通过合并两个数据框来查找匹配的行
merged_data = data1.merge(data2, left_on=['Author', 'c_assoc_person'], right_on=['姓名', '社會關係人姓名'], how='left',
                          indicator=True)  # indicator=True会将合并的记录放在新的一列

# 创建一个新的列来指示每一行是否有一个匹配的行在另一个CSV文件中
merged_data['MatchInOtherCSV'] = merged_data['_merge'] == 'both'

# 删除_merge列，因为我们不再需要它
merged_data.drop('_merge', axis=1, inplace=True)

# 保存结果到一个新的CSV文件
merged_data.to_csv('社会关系_output_result.csv', index=False, encoding='utf-8-sig')
