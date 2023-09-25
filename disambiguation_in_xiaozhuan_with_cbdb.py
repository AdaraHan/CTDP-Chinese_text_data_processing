"""author:Adara 2023/7/11
需求：对小传中的人物按照进士年、字号、籍贯等信息进行消歧
思路：
1. 提取小传中的字、号、籍贯、进士年信息
2. cbdb中的入仕年与小传中的入仕年按照cbdb的id进行匹配
3. 比较“進士”列的值是否与“c_year”列的值重合
4. 比较“字”、“號”、“籍贯”三列的值是否与“contents_matched”列的值有重合，并计算重合个数
5. 根据进士年和“字”、“號”、“籍贯”三列的值，修改“decition”列的值
6. 把修改后的“decition”列的值更新到原来的大表：merged_rengong_cbdb_0627【最新版一律存储为latest】
"""
import csv
import re


# 从小传中提取字号、籍贯等信息
def extract_zihao_jiguan_jinshinian(inputfile, output_file):
    # 从小传中提取籍贯信息
    def extract_location(text):
        matches = re.findall(r'，([^，]+)（', text)
        if matches:
            return matches[-1]
        else:
            return ''

    # 将中文数字转换为阿拉伯数字
    def convert_to_roman(year):
        # 去掉小括号
        year = re.sub(r'[（）]', '', year)
        roman_mapping = {
            '○': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        # 将中文数字转换为阿拉伯数字
        for key, value in roman_mapping.items():
            year = year.replace(key, str(value))
        return year

    # 读取csv文件
    with open(inputfile, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

        header = rows[0]
        xiaozhuan_y_index = header.index('xiaozhuan_y')

        # 添加新的列
        new_header = header + ['字', '號', '籍贯', '進士']
        new_rows = [new_header]

        # 正则匹配字号、籍贯信息
        for row in rows[1:]:
            xiaozhuan_y_text = row[xiaozhuan_y_index]
            match_zi = re.search(r'(?<=字).*?(?=，)', xiaozhuan_y_text)
            match_hao = re.search(r'(?<=號).*?(?=，)', xiaozhuan_y_text)
            match_jiguan = re.search(r'(?<=，).+?(?=（*）人)', xiaozhuan_y_text)
            match_jinshi = re.search(r'......(?=進士)', xiaozhuan_y_text)

            location = extract_location(match_jiguan.group(0)) if match_jiguan else ''
            year = convert_to_roman(match_jinshi.group(0)) if match_jinshi else ''

            new_row = row[:]  # new_row = row[:] 来创建 new_row 的副本，以免在后续的迭代过程中改变了原始的行数据。
            new_row.append(match_zi.group(0) if match_zi else '')
            new_row.append(match_hao.group(0) if match_hao else '')
            new_row.append(location)
            new_row.append(year)

            new_rows.append(new_row)

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as file:  # newline='' 用于解决输出文件中的空行问题
        writer = csv.writer(file)
        writer.writerows(new_rows)

    print("处理完成，结果保存在", output_file, "文件中。")


# cbdb中的入仕年与小传中的入仕年按照cbdb的id进行匹配
def add_c_year_column(output_file, entry_data_file):
    # 读取 output.csv 文件
    with open(output_file, 'r', encoding='utf-8-sig') as output_csv:
        output_reader = csv.reader(output_csv)
        output_rows = list(output_reader)

        output_header = output_rows[0]
        id_cbdb_index = output_header.index('id_cbdb')

        # 读取 ENTRY_DATA.csv 文件
        with open(entry_data_file, 'r', encoding='utf-8-sig') as entry_data_csv:
            entry_data_reader = csv.reader(entry_data_csv)
            entry_data_rows = list(entry_data_reader)

            entry_data_header = entry_data_rows[0]
            c_personid_index = entry_data_header.index('c_personid')
            c_year_index = entry_data_header.index('c_year')

            # 获取相应的 c_year 列数据
            c_year_values = {}
            for entry_row in entry_data_rows[1:]:
                c_personid = entry_row[c_personid_index]
                c_year = entry_row[c_year_index]
                c_year_values[c_personid] = c_year

            # 在 output_rows 中新增一列存放相应的 c_year 值
            new_output_header = output_header + ['c_year']
            new_output_rows = [new_output_header]

            for output_row in output_rows[1:]:
                id_cbdb = output_row[id_cbdb_index]
                c_year = c_year_values.get(id_cbdb, '')
                new_output_row = output_row + [c_year]
                new_output_rows.append(new_output_row)

            # 写入结果到新的文件 output_with_c_year.csv
            output_with_c_year_file = 'output_with_c_year.csv'
            with open(output_with_c_year_file, 'w', encoding='utf-8-sig', newline='') as result_csv:
                result_writer = csv.writer(result_csv)
                result_writer.writerows(new_output_rows)

            print("处理完成，结果保存在", output_with_c_year_file, "文件中。")


# 比较“進士”列的值是否与“c_year”列的值重合
def compare_jinshi_and_c_year(output_file):
    # 读取 output_with_c_year.csv 文件
    with open(output_file, 'r', encoding='utf-8-sig') as output_csv:
        output_reader = csv.reader(output_csv)
        output_rows = list(output_reader)

        output_header = output_rows[0]
        jinshi_index = output_header.index('進士')
        c_year_index = output_header.index('c_year')

        # 在 output_rows 中新增一列 "result_entry_year"
        new_header = output_header + ['result_entry_year']
        new_rows = [new_header]

        for output_row in output_rows[1:]:
            jinshi_value = output_row[jinshi_index]
            c_year_value = output_row[c_year_index]

            # 比较 "進士" 列与 "c_year" 列的值
            if jinshi_value == c_year_value and jinshi_value != '' and c_year_value != '':
                result_entry_year = 'same'
            elif jinshi_value != c_year_value and (jinshi_value != '' or c_year_value != ''):
                result_entry_year = 'different'
            else:
                result_entry_year = 'null'

            new_row = output_row + [result_entry_year]
            new_rows.append(new_row)

        # 写入结果到新的文件 output_with_result_entry_year.csv
        output_with_result_entry_year_file = 'output_with_result_entry_year.csv'
        with open(output_with_result_entry_year_file, 'w', encoding='utf-8-sig', newline='') as result_csv:
            result_writer = csv.writer(result_csv)
            result_writer.writerows(new_rows)

        print("处理完成，结果保存在", output_with_result_entry_year_file, "文件中。")


# 比较“字”、“號”、“籍贯”三列的值是否与“contents_matched”列的值有重合
def compare_contents_matched(output_file):
    # 读取 output_with_result_entry_year.csv 文件
    with open(output_file, 'r', encoding='utf-8-sig') as output_csv:
        output_reader = csv.reader(output_csv)
        output_rows = list(output_reader)

        output_header = output_rows[0]
        contents_matched_index = output_header.index('contents_matched')
        zi_index = output_header.index('字')
        hao_index = output_header.index('號')
        jiguan_index = output_header.index('籍贯')

        # 在 output_rows 中新增一列 "result_zihao_jiguan"
        new_header = output_header + ['result_zihao_jiguan']
        new_rows = [new_header]

        for output_row in output_rows[1:]:
            contents_matched_value = output_row[contents_matched_index]
            zi_value = output_row[zi_index]
            hao_value = output_row[hao_index]
            jiguan_value = output_row[jiguan_index]

            # 按分号分隔 contents_matched_value 的多个值
            contents_matched_values = contents_matched_value.split(';')

            # 判断每个值是否与 zi_value、hao_value、jiguan_value 有重合
            match_count = 0
            for value in contents_matched_values:
                if value == zi_value or value == hao_value or value == jiguan_value:
                    match_count += 1

            new_row = output_row + [match_count]
            new_rows.append(new_row)

        # 写入结果到新的文件 output_with_result_zihao_jiguan.csv
        output_with_result_zihao_jiguan_file = 'output_with_result_zihao_jiguan.csv'
        with open(output_with_result_zihao_jiguan_file, 'w', encoding='utf-8-sig', newline='') as result_csv:
            result_writer = csv.writer(result_csv)
            result_writer.writerows(new_rows)

        print("处理完成，结果保存在", output_with_result_zihao_jiguan_file, "文件中。")


# 根据进士年和“字”、“號”、“籍贯”三列的值，修改“decition”列的值
def modify_decision(output_file):
    # 读取 output_with_result_zihao_jiguan.csv 文件
    with open(output_file, 'r', encoding='utf-8-sig') as output_csv:
        output_reader = csv.reader(output_csv)
        output_rows = list(output_reader)

        output_header = output_rows[0]
        result_entry_year_index = output_header.index('result_entry_year')
        result_zihao_jiguan_index = output_header.index('result_zihao_jiguan')
        decision_index = output_header.index('decision')

        for output_row in output_rows[1:]:
            result_entry_year_value = output_row[result_entry_year_index]
            result_zihao_jiguan_value = output_row[result_zihao_jiguan_index]
            decision_value = output_row[decision_index]

            # 修改 "decision" 列的值为 '_y'，如果满足条件
            if result_entry_year_value == 'same' or result_zihao_jiguan_value != '0':
                output_row[decision_index] = '_y'

        # 写入结果到新的文件 output_with_result_zihao_jiguan.csv
        output_final_file = 'output_final.csv'
        with open(output_final_file, 'w', encoding='utf-8-sig', newline='') as result_csv:
            result_writer = csv.writer(result_csv)
            result_writer.writerows(output_rows)

        print("处理完成，结果保存在", output_final_file, "文件中。")


def update_decision(merged_file, output_final_file):
    # 读取 output_final.csv 文件
    with open(output_final_file, 'r', encoding='utf-8-sig') as final_csv:
        final_reader = csv.reader(final_csv)
        final_rows = list(final_reader)

        final_header = final_rows[0]
        decision_index = final_header.index('decision')
        id_souyun_index = final_header.index('id_souyun')

        # 创建字典，用于存储 id_souyun 和 decision 值的对应关系
        decision_dict = {}
        for final_row in final_rows[1:]:
            id_souyun_value = final_row[id_souyun_index]
            decision_value = final_row[decision_index]
            decision_dict[id_souyun_value] = decision_value

    # 更新 merged_rengong_cbdbid_0627.csv 文件中的 decision 列
    with open(merged_file, 'r', encoding='utf-8-sig') as merged_csv:
        merged_reader = csv.reader(merged_csv)
        merged_rows = list(merged_reader)

        merged_header = merged_rows[0]
        decision_index = merged_header.index('decision')
        id_souyun_index = merged_header.index('id_souyun')

        for merged_row in merged_rows[1:]:
            id_souyun_value = merged_row[id_souyun_index]
            if id_souyun_value in decision_dict:
                decision_value = decision_dict[id_souyun_value]
                merged_row[decision_index] = decision_value

    # 保存更新后的结果到 merged_rengong_cbdbid_0627_updated.csv 文件
    with open('merged_rengong_cbdbid_0711.csv', 'w', encoding='utf-8-sig', newline='') as updated_csv:
        updated_writer = csv.writer(updated_csv)
        updated_writer.writerows(merged_rows)

    print("处理完成，结果保存在 merged_rengong_cbdbid_0711.csv 文件中。")


# 调用函数并传入文件名
extract_zihao_jiguan_jinshinian('input.csv', 'output.csv')
add_c_year_column('output.csv', 'ENTRY_DATA.csv')
compare_jinshi_and_c_year('output_with_c_year.csv')
compare_contents_matched('output_with_result_entry_year.csv')
modify_decision('output_with_result_zihao_jiguan.csv')
update_decision('merged_rengong_cbdbid_0627.csv', 'output_final.csv')
