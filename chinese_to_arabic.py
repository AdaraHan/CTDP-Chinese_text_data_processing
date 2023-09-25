import pandas as pd

# 中文数字到阿拉伯数字的映射
# 【注意】先在原csv文件中把“○”转为“零”
CN_NUM = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
}

CN_UNIT = {
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000,
}


# 转生卒年
def chinese_to_arabic_direct(cn) -> int:
    if not isinstance(cn, str):
        return cn  # 如果不是字符串，直接返回原值
    cn_str = str(cn)  # 确保cn是字符串
    arabic_list = [CN_NUM.get(char, str(char)) for char in cn_str]
    # 调试输出：
    print(f"Original: {cn_str}, Transformed: {arabic_list}")
    arabic_str = ''.join(str(i) for i in arabic_list)
    print(f"Original: {cn_str}, Transformed: {arabic_str}")
    try:
        return int(arabic_str)
    except ValueError:
        return arabic_str  # 如果转换不成功，返回字符串格式


# 转享年
def chinese_to_arabic(cn: str) -> int:
    if not isinstance(cn, str):
        return cn  # 如果不是字符串，直接返回原值

    # 如果“十”或“百”出现在第一个位置，则在其前面添加“一”，解决十七转为7、百三十转为30的问题。
    if cn.startswith("十") or cn.startswith("百"):
        cn = "一" + cn

    unit = 0  # 默认单位是0
    ldig = []  # 保存转换的数字

    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            if cndig == '十' and unit == 1:
                ldig.append(unit)  # 对于“十一”这样的数字，处理十的单位
            unit = CN_UNIT.get(cndig)
        else:
            num = CN_NUM.get(cndig)
            if num is None:
                raise ValueError(f"Unrecognized Chinese numeral: {cndig}")
            if unit:
                num *= unit
                unit = 1  # 重置单位为1
            ldig.append(num)
    return sum(ldig)


# 读取CSV文件
df = pd.read_csv('生卒享年_input.csv', encoding='utf-8')

# 将“生年”和“卒年”列转换为阿拉伯数字
df['生年'] = df['生年（大写）'].apply(chinese_to_arabic_direct)
df['卒年'] = df['卒年（大写）'].apply(chinese_to_arabic_direct)
# 将“享年”列转换为阿拉伯数字
df['享年'] = df['享年（大写）'].apply(chinese_to_arabic)
# 将结果保存回CSV文件
df.to_csv('生卒享年_output.csv', index=False, encoding='utf-8-sig')
