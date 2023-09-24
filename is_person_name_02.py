"""author: Adara 2023/4/5
需求：筛选output-newpeople.xls表姓名列（author）中文字符总数小于4的数据里，包含称谓、官职的数据。
"""
import pandas as pd

df = pd.read_excel('output_newpeople_character3.xls')


def is_person_name(name):
    non_person_names = ['处士', '公主', '太后', '員外', '先輩', '公', '生', '師', '相公', '長官', '徵君', '徵士',
                        '神童', '將軍', '尊师', '道者',
                        '道士', '道人大師', '僧', '逸人', '三藏', '禪師', '長老', '律師', '禪翁', '禪友', '座主',
                        '上人', '僧', '子', '女', '姥',
                        '觀主', '煉師', '明府', '補闕', '郎中', '供奉', '內召', '詹事', '秘（祕）書', '學士', '從事',
                        '支使', '判官', '侍御', '拾遺',
                        '使君', '評事', '推官', '太傅', '中丞', '太祝', '録事', '少府', '主簿', '尚書', '協律', '司戶',
                        '功曹', '司錄', '參軍', '別駕',
                        '秀才', '五經', '孝廉', '太守', '文學']
    for non_person_name in non_person_names:
        if non_person_name in name:
            return False
    return True


df['is_person_name'] = df['author'].apply(lambda x: is_person_name(x))

df.to_excel('output_newpeople_character3_name_judgment.xls', index=False)
