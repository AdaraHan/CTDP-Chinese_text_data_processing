"""
需求：匹配两个有关系的人名是否在同一个百度百科页面或维基百科页面中出现
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from opencc import OpenCC
import wikipediaapi
import time

# 用你的CSV文件路径替换以下路径
csv_file_path = "社会关系_input.csv"

# 读取CSV文件
data = pd.read_csv(csv_file_path, encoding='utf-8')

# 初始化OpenCC来进行繁体到简体的转换
cc = OpenCC('t2s')

# 设置维基百科API
wiki_wiki = wikipediaapi.Wikipedia(
    language='ZH',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='my_python_app',
    timeout=10
)


def check_names_in_wikipedia(row):
    # 获取当前行的两个名字
    # name1 = cc.convert(row['Author'])
    # name2 = cc.convert(row['c_assoc_person'])
    name1 = row['Author']
    name2 = row['c_assoc_person']

    try:
        page = wiki_wiki.page(name1)
        if page.exists():
            return name2.lower() in page.text.lower()
        else:
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}. Retrying...")
        time.sleep(5)  # 等待5秒钟再试


# 【方法一】结果全部为TRUE
def check_names_in_baidu(row):
    name1 = cc.convert(row['Author'])
    name2 = cc.convert(row['c_assoc_person'])
    # name1 = row['Author']
    # name2 = row['c_assoc_person']

    # 构建用于百度百科搜索的URL
    url = f"https://baike.baidu.com/search?word={name1}+{name2}"

    try:
        # 发送请求
        response = requests.get(url)

        # 检查响应状态
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 从搜索结果页面中提取文本
            # 注意：这里的选择器可能需要根据实际页面结构进行调整
            text = " ".join([p.get_text() for p in soup.find_all('p')])

            # 检查两个名字是否都出现在摘要中
            return name1.lower() in text.lower() and name2.lower() in text.lower()
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# 【方法二】
def check_names_in_baidu_baike(row):
    # 获取当前行的两个名字，并将它们从繁体转换为简体
    name1 = cc.convert(row['Author'])
    name2 = cc.convert(row['c_assoc_person'])

    # 尝试获取包含第一个名字的百度百科页面
    try:
        response = requests.get(f"https://baike.baidu.com/item/{name1}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return False

    # 检查第二个名字是否出现在该页面上
    return name2 in response.text


# 对CSV文件中的每一行应用函数，并创建一个新的列来存储结果
data['InSameWikiPage'] = data.apply(check_names_in_wikipedia, axis=1)
data['InSameBaiduPage'] = data.apply(check_names_in_baidu, axis=1)
data['InSameBaikePage'] = data.apply(check_names_in_baidu_baike, axis=1)

# 保存结果到一个新的CSV文件
data.to_csv('社会关系_output.csv', index=False, encoding='utf-8-sig')
