"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import os
import re
from pathlib import Path
import chardet


def get_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    files = list(map(str, sorted(Path(base_path).glob('info_*'))))
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    for file in files:
        with open(file, 'rb') as f:
            file = f.read()
            file = file.decode(chardet.detect(file)['encoding'])
            os_prod_list.append(re.sub(r'Изготовитель системы:\s+', '', re.findall(r'Изготовитель системы:\s+\w+', file)[0]))
            os_name_list.append(re.sub(r'Название ОС:\s+', '', re.findall(r'Название ОС:\s+\w+', file)[0]))
            os_code_list.append(re.sub(r'Код продукта:\s+', '', re.findall(r'Код продукта:\s+\w+', file)[0]))
            os_type_list.append(re.sub(r'Тип системы:\s+', '', re.findall(r'Тип системы:\s+\w+', file)[0]))
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for i in range(len(files)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data


def write_to_csv(path_to_csv):
    with open(path_to_csv, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f_writer.writerows(get_data())


write_to_csv('data_report.csv')
