"""author: Adara 2023/4/4
需求：搜韵json数据转成csv【结果命名为CNKGraph.Writings_02.csv】
"""
import json
import csv

# 打开json文件
with open('CNKGraph.Writings.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# 获取列名
keys = set()
for item in data['Items']:
    keys.update(item.keys())

# 写入csv文件
with open('CNKGraph.Writings_output.csv', mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    for item in data['Items']:
        writer.writerow(item)


