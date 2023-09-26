"""author: Adara 2022/5/1
需求：将《全宋诗》PDF文本拆分为单页PDF文件，并生成CSV文件
"""
import os
import csv
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

input_pdf = 'C:/Users/92163/Desktop/QTS&QSS/《全宋诗》PDF文本/拆页/72[45703].pdf'
output_csv = 'output_72.csv'
output_folder = 'C:/Users/92163/Desktop/QTS&QSS/《全宋诗》PDF文本/拆页/72[45703]/'


def split_and_rename_pdf(input_pdf, output_folder):
    with open(input_pdf, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            pdf_writer = PdfWriter()
            new_page_num = page_num + 1 - 72 + 45100  # 减去目录及封面页，加上前面的页数

            if new_page_num > 45100:
                pdf_writer.add_page(pdf_reader.pages[page_num])

                output_filename = os.path.join(output_folder, f"{new_page_num}.pdf")
                with open(output_filename, "wb") as output_file:
                    pdf_writer.write(output_file)


def generate_csv(input_pdf, output_folder):
    with pdfplumber.open(input_pdf) as pdf:
        num_pages = len(pdf.pages)

        with open(os.path.join(output_folder, output_csv), 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['page', 'book', 'file_name'])

            for page_num in range(num_pages):
                new_page_num = page_num + 1 - 72 + 45100

                if new_page_num > 45100:
                    file_name = f"{new_page_num}.pdf"
                    csv_writer.writerow([new_page_num, '72', file_name])


if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件夹路径
    os.chdir(folder_path)  # 将当前文件夹路径设置为工作路径
    # input_pdf = input("请输入要拆分的PDF文件名：")

    split_and_rename_pdf(input_pdf, output_folder)  # 拆分PDF文件
    generate_csv(input_pdf, folder_path)  # 生成CSV文件
    print("PDF拆分完成，结果已写入CSV文件。")  # 打印提示信息
