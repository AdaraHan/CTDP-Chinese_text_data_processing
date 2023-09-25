"""author:Adara 2023.07.24
需求：《全宋诗》中诗歌作者与诗题人物的社会网络关系
思路：
1. 合并诗题人物与诗歌作者数据
2. 诗题人物与诗歌作者的社会网络关系
3. 修改程序，使得输出结果times一个标题只计算一次【2023.08.14已完成】
"""
import pandas as pd
import time


# 1. 合并诗题人物与诗歌作者数据
def merge_name_author(output):
    df1 = pd.read_csv('merged_rengong_cbdbid_latest.csv', encoding='utf-8')
    df2 = pd.read_csv('name_in_title.csv', encoding='utf-8')

    print("Columns in df1: ", df1.columns)
    print("Columns in df2: ", df2.columns)

    merge_df = pd.merge(df1, df2, how='left', on='id_title')
    merge_df.to_csv(output, encoding='utf-8-sig', index=False)


# 2. 诗题人物与诗歌作者的社会网络关系
def social_network(input):
    # 读取csv文件
    df_A = pd.read_csv(input, encoding='utf-8-sig')
    df_B = pd.read_csv('social_network_song_0602.csv', encoding='utf-8-sig')

    # 创建一个set用于快速查找
    social_network_set = set(df_B[['姓名', '社會關係人姓名']].apply(frozenset, axis=1).tolist())

    # 不考虑顺序，比较A文档中的姓名两列是否在B文档中的姓名两列中
    df_A['social_network_Author'] = df_A.apply(
        lambda row: 'is' if frozenset([row['Author'], row['name_in_title']]) in social_network_set else 'no',
        axis=1)
    print(df_A['social_network_Author'])

    # 标题姓名列中每个名字匹配到 'is' 的次数
    df_is = df_A[df_A['social_network_Author'] == 'is']
    print('df_is=', df_is)

    # 删除df_is中title_y列中的重复值
    df_is = df_is.drop_duplicates(subset=['title_y'], keep='first')
    print('df_is删除重复值后：', df_is)

    # 统计df_is中title_y列中每个名字出现的次数
    count_is = df_is.groupby('name_in_title').size()  # size()函数：返回分组后的组大小
    print('count_is=', count_is)

    df_A['times_name'] = df_A['name_in_title'].map(count_is)  # map()函数：根据提供的函数对指定序列做映射

    # 保存为csv文件
    df_A.to_csv('output_sna_qss.csv', index=False, encoding='utf-8-sig')


start_time = time.time()

merge_name_author('output_merged_rengong_cbdbid_latest_name_in_title.csv')
social_network('output_merged_rengong_cbdbid_latest_name_in_title.csv')

end_time = time.time()

print("The entire program took %s seconds" % (end_time - start_time))
