import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import multiprocessing as mp

# global data for graph
x_data, y_data = [], []

def show(avg, stop_graph):
    """Show graph."""
    global x_data, y_data
    start = datetime.now()
    data_limit = 50
    time_interval = 200

    def update(frame):
        if len(x_data) > data_limit:
            x_data.pop(0)
            y_data.pop(0)

        if stop_graph.value == 0:
            x_data.append((datetime.now()-start).total_seconds() * 1000)
            y_data.append(avg.value)
            plt.cla()
            plt.plot(x_data, y_data)
            plt.xlabel("time(ms)")
            plt.ylabel("intensity")

    animation = FuncAnimation(plt.gcf(), update, interval=time_interval)

    plt.tight_layout()
    plt.show()

def run(avg, stop_graph):
    """Run Nail Detection."""
    # reading the video
    source = cv2.VideoCapture(0)

    # running the loop
    while True:

        # extracting the frames
        ret, img = source.read()
        
        # converting to gray-scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
        gray = cv2.rectangle(gray, (w_c-100, h_c+100), (w_c+100, h_c-100), (255, 255, 255), 2)

        # get intensity (white 255 -> black 0)
        # print(gray[h_c-100+5:h_c+100-5, w_c-100+5:w_c+100-5])
        avg.value = np.average(gray[h_c-100+5:h_c+100-5, w_c-100+5:w_c+100-5])
        print(avg.value)

        # displaying the video
        cv2.imshow("Nail Detection Live", gray)

        # exiting the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            stop_graph.value = 1
            break
        
    # closing the window
    cv2.destroyAllWindows()
    source.release()

if __name__=='__main__':
    avg = mp.Value('d', 0.0)
    stop_graph = mp.Value('i', 0)
    p1 = mp.Process(target=show, args=(avg, stop_graph))
    p1.start()
    p2 = mp.Process(target=run, args=(avg, stop_graph))
    p2.start()
    p1.join()
    p2.join()

    