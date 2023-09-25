import pandas as pd
from opencc import OpenCC

# 读取两个csv文件
df_a = pd.read_csv('shixu_qss_merged_both_latest.csv', encoding='utf-8-sig')
df_b = pd.read_csv('souyun_song.csv', encoding='utf-8-sig')

# 创建OpenCC对象，进行繁体到简体的转换
cc = OpenCC('t2s')

# 将两个文档中的“作者”“title”列从中文繁体转为中文简体
df_a['作者_简体'] = df_a['作者'].apply(cc.convert)
df_a['title_简体'] = df_a['title'].apply(cc.convert)

df_b['Author_简体'] = df_b['Author'].apply(cc.convert)
df_b['Title_简体'] = df_b['Title'].apply(cc.convert)

# 重新命名B文本中的列以便和A文本中的列名对应
df_b.rename(columns={'Author_简体': '作者_简体', 'Title_简体': 'title_简体'}, inplace=True)

# 合并两个DataFrame，如果A文本中有“作者_简体”“title_简体”列与B文本中有“作者_简体”“title_简体”列完全相同，则将B文本中有“作者”“title”列对应的“id_souyun”列写入新的DataFrame
df_new = pd.merge(df_a, df_b[['作者_简体', 'title_简体', 'id_souyun']], on=['作者_简体', 'title_简体'], how='left')

# 将新的DataFrame写入新的csv文件
df_new.to_csv('merge_shixu_qss_with_souyun_song.csv', index=False, encoding='utf-8-sig')
