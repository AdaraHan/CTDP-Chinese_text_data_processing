import csv

output = []
with open("all_qss_gai.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()  # 清除行首行尾的空格和换行符
    if line.endswith(("序", "引", "叙", "敘")):  # 检查行是否以给定的任何词结束
        seq_name = line  # 保存序名
        i += 1  # 转到下一行
        while i < len(lines) and len(lines[i].strip()) <= 20:
            i += 1  # 如果下一行字符数不大于20，则转到再下一行
        if i < len(lines):
            seq = lines[i].strip()  # 保存序
            output.append((seq_name, seq))  # 添加结果到output列表
    i += 1

# 将结果写入CSV文件
with open("output_content_shixu.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["序名", "序"])  # 写入标题
    writer.writerows(output)  # 写入结果
