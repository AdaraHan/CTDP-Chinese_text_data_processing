import pandas as pd

# 读取原始CSV文件
file_path = 'CNKGraph.Writings_02_add_cleaned.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 指定要搜索的列名
column_name = 'Dynasty'

# 定义包含特定内容的关键词列表
keywords = ['宋', '五代', '後梁', '後唐', '後晋', '後汉', '後周', '楚', '南漢', '蜀', '吳越', '南唐', '吳', '閩', '荊南', '北漢',
            '南平', '金', '遼', '西夏']


# 查找包含关键词的行
def contains_keyword(text, keywords):
    for keyword in keywords:
        if keyword in text:
            return True


# 应用函数并筛选结果
filtered_df = df[df[column_name].apply(lambda x: contains_keyword(str(x), keywords))]
print("筛选结果：", filtered_df.shape)

# 将结果保存到新的CSV文件
output_file_path = 'CNKGraph.Writings_02_add_cleaned_song.csv'
filtered_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
print("处理完成，结果已保存到:", output_file_path)
