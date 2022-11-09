import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

NUMBER_OF_FRAME = 20

def adjust_frame(frame):
    # converting to gray-scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # crop image
    width = gray.shape[1]
    height = gray.shape[0]
    w_c = width // 2
    h_c = height // 2
    gray = gray[h_c-50:h_c+50, w_c-50:w_c+50]

    # resize image
    gray = cv2.resize(gray, (width, height), interpolation = cv2.INTER_AREA)

    # mirror image
    gray = cv2.flip(gray, 1)

    # draw a rectangle
    new_frame = cv2.rectangle(gray, (w_c-100, h_c+100), (w_c+100, h_c-100), (255, 255, 255), 2)

    value_intensity = np.average(gray[h_c-100+5:h_c+100-5, w_c-100+5:w_c+100-5])

    return (new_frame, value_intensity)


def compare_frame(data_frames):
    for i in range(0, NUMBER_OF_FRAME-1):
        if data_frames[i] != data_frames[i+1]:
            break
        else:
            print(f'{i} == {i+1}')


def get_frames():
    data = []

    # reading the video
    source = cv2.VideoCapture(0)

    # running the loop
    while len(data) == NUMBER_OF_FRAME:

        # extracting the frames
        ret, img = source.read()

        frame, value_intensity = adjust_frame(img)
        
        data.append(value_intensity)

        # displaying the video
        cv2.imshow("Nail Detection Live", frame)

        
    # closing the window
    cv2.destroyAllWindows()
    source.release()

    print(data)

    # compare_frame(data)



def main():
    get_frames()



if __name__=='__main__':
    main()
    