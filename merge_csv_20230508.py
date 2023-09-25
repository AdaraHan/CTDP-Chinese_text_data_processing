import pandas as pd

# 读取CSV文件
file_a = pd.read_csv('【人工】souyun_song_matchqss_quchong_mergedxiaozhuan_xiaoqi_merge.csv', encoding='utf-8-sig')
file_b = pd.read_csv('souyun_song.csv', encoding='utf-8-sig')

# 使用'AuthorId'列将两个文件合并
merged_file = pd.merge(file_a, file_b, on='AuthorId', how='left')

# 将合并后的文件保存为CSV
merged_file.to_csv('【人工】souyun_song_matchqss_mergedxiaozhuan_xiaoqi_merge.csv', index=False, encoding='utf-8-sig')

