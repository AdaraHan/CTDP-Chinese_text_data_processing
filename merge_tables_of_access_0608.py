import pandas as pd
import pyodbc

# 定义数据库连接字符串
database_file = "D:\\Document\\SynologyDrive\\2023年6月后\\merge_cbdbid_souyunrengong_0608.accdb"
conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database_file + ';'
)

# 使用pyodbc连接到Access数据库
conn = pyodbc.connect(conn_str)

# 使用pandas读取两个数据表
df1 = pd.read_sql_query('SELECT * FROM rengong_souyun', conn)
df2 = pd.read_sql_query('SELECT * FROM compareResultList_cbdbid', conn)

# 检查两个数据表的列名
print("Columns in rengong_souyun: ", df1.columns)
print("Columns in compareResultList_cbdbid: ", df2.columns)

# # 去除列名中的空格
# df1.columns = df1.columns.str.strip()
# df2.columns = df2.columns.str.strip()

# 按照 author 和 title 列进行合并，保留所有数据（相同和不同的数据）
merged_df = pd.merge(df1, df2, left_on=['Author', 'title'], right_on=['author', 'title'], how='outer')

# 输出合并后的数据
print(merged_df)

# 将合并后的数据保存到新的数据表中
# merged_df.to_sql('merged_rengong_cbdbid', conn, if_exists='replace', index=False)

# 将合并后的数据保存为CSV文件
merged_df.to_csv('merged_rengong_cbdbid.csv', index=False, encoding='utf-8-sig')

# 关闭数据库连接
conn.close()
