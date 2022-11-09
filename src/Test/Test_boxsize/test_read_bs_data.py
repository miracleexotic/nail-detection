"""
อ่านข้อมูลจากไฟล์ CSV ที่บันทึกโดยไฟล์ test_write_bs_data.py

ข้อมูลจาก database folder
"""

import pathlib
import csv
from pprint import pprint
import re
from matplotlib import pyplot as plt

def read_from_csv(path: str):
    """อ่านข้อมูลจากไฟล์ csv"""
    data = []
    with open(path, 'r') as f:
        csv_in = csv.reader(f)
        data = [row for row in csv_in]

    return data

def extract_data(data: list):
    """แยกข้อมูลจาก data_graph column"""
    regex = r"\((.*?,.*?)\)"
    for row in data:
        matches = re.finditer(regex, row[2], re.MULTILINE)
        match_list = [tuple(map(float, x.group().lstrip('(').strip(')').split(','))) for x in matches]
        # print(f'{int(row[3])} == {len(match_list)} {int(row[3]) == len(match_list)}')
        # print(match_list)
        row[2] = match_list
    
    return data

def plot_graph(data: list):
    data_graph = data[2]
    plt.plot(*zip(*data_graph))
    plt.ylim([0, 255])
    plt.xlabel("time(ms)")
    plt.ylabel("intensity")
    plt.show()



if __name__ == '__main__':
    data = read_from_csv(r'C:\Users\IAMMAI\Desktop\githubProject\NailsDetection\src\Database\DB_test_boxsize\rpi4\data_01102022_135742.csv')
    data = extract_data(data)
    # pprint(data)
    for row in data:
        print(row[0])
        plot_graph(row)


