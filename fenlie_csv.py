import pandas as pd


def split_column_by_space(file_name, column_name, encodings='UTF-8-SIG'):
    # 读取csv文件
    df = pd.read_csv(file_name, encoding=encodings)

    # 检查该列是否存在
    if column_name not in df.columns:
        print(f"列 {column_name} 在数据框中不存在。")
        return

    # 对目标列进行分列
    split_data = df[column_name].str.split('\t', expand=True)

    # 将分列后的数据合并回原始数据框
    for i in range(split_data.shape[1]):
        df[f"{column_name}_{i}"] = split_data[i]

    # 保存新的csv文件
    df.to_csv('new_' + file_name, index=False, encoding=encodings)

    print(f"处理完毕，新的csv文件已经保存为 'new_{file_name}'.")


# 通过文件名和列名调用函数
split_column_by_space('compareResultList_0602.csv', 'original', encodings='UTF-8-SIG')
