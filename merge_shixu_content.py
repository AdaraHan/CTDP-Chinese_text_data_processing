import pandas as pd

# 读取文件
output_df = pd.read_csv('output_content_shixu.csv', encoding='utf-8-sig')
merge_df = pd.read_csv("merge_shixu_qss_with_souyun_song.csv", encoding='utf-8-sig')

# 创建一个以 "序名" 为键，"序" 为值的字典
seq_dict = output_df.set_index('序名')['序'].to_dict()

# 在 merge_df 中遍历每行，查找并设置 "序" 的值
merge_df['序'] = merge_df['序名'].map(seq_dict)

# 输出新的文档
merge_df.to_csv("output_content_merge_shixu_qss_with_souyun_song.csv", index=False, encoding='utf-8-sig')
