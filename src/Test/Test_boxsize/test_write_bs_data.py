"""
บันทึกข้อมูลลงไฟล์ CSV เก็บที่ database folder
"""

import cv2
import numpy as np
from datetime import datetime
from time import time
import csv
import pathlib


TIME_TO_LIVE = 5 # seconds

def adjust_frame(frame, box_size: int):
    """ปรับปรุง frame ที่รับเข้ามา"""
    # converting to gray-scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # crop image
    width = gray.shape[1]
    height = gray.shape[0]
    # center pos
    w_c = width // 2
    h_c = height // 2
    # zoom
    gray = gray[h_c-50:h_c+50, w_c-50:w_c+50]

    # resize image
    gray = cv2.resize(gray, (width, height), interpolation = cv2.INTER_AREA)

    # mirror image
    gray = cv2.flip(gray, 1)

    # calculate intensity
    size = box_size // 2
    value_intensity = np.average(gray[h_c-size:h_c+size, w_c-size:w_c+size])
    
    # draw a rectangle
    new_frame = cv2.rectangle(gray, (w_c-size, h_c+size), (w_c+size, h_c-size), (255, 255, 255), 2)

    return (new_frame, value_intensity)


def get_frames(box_size: int):
    data = []

    # reading the video
    source = cv2.VideoCapture(0)

    prev_time = time()
    curr_time = time()

    # running the loop
    while curr_time - prev_time < TIME_TO_LIVE:

        curr_time = time()

        # extracting the frames
        ret, img = source.read()
        frame, value_intensity = adjust_frame(img, box_size)

        new_data = (curr_time - prev_time, value_intensity)
        data.append(new_data)

        # displaying the video
        cv2.imshow("Nail Detection Live", frame)
        cv2.waitKey(1)
        
    # closing the window
    cv2.destroyAllWindows()
    source.release()

    return data


def data_to_string(data):
    """แปลงข้อมูลพิกัดให้เก็บในรูปแบบ string ของ data_graph ลงในไฟล์ csv"""
    data_string = "["
    for t_data, i_data in data:
        data_string += f"({t_data},{i_data}),"
    data_string = data_string[:-1]
    data_string += "]"

    return data_string

def data_to_csv(data):
    """บันทึกไฟล์ลง csv"""
    path_to_database = pathlib.Path(__file__).parent.parent / "database"
    datetime_str = datetime.now().strftime("%d%m%Y_%H%M%S")
    filename = path_to_database / f"data_{datetime_str}.csv"
    with open(filename, 'w', newline='') as f:
        csv_out = csv.writer(f)
        csv_out.writerows(data)

def main():
    data = []
    size = 30
    size_step = 5
    index_number = 3

    for index in range(0, index_number):
        new_data = get_frames(size)
        data.append((index, size, data_to_string(new_data), len(new_data)))
        size += size_step

    data_to_csv(data)


if __name__=='__main__':
    main()
    