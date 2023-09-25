import dask.dataframe as dd

# 读取CSV文件
file_a = dd.read_csv('compareResultList_merge_title_final_0602.csv', encoding='utf-8-sig')
file_b = dd.read_csv('【人工】souyun_song_matchqss_mergedxiaozhuan_xiaoqi_merge_shaixuan_2023.6.6.csv', encoding='utf-8-sig')

# 使用'xiaozhuan'列将两个文件合并
merged_file = dd.merge(file_a, file_b, on='xiaozhuan', how='left')

# 将合并后的文件保存为CSV
merged_file.to_csv('compareResultList_merge_title_final_merge_rengong_0607.csv', index=False, encoding='utf-8-sig')

