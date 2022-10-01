from time import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

def get_fps():
    data = []

    # reading the video
    source = cv2.VideoCapture(0)

    count = 0
    prev_time = time()
    # running the loop
    while time() - prev_time < 1:

        # extracting the frames
        ret, img = source.read()
        count += 1

        # displaying the video
        # cv2.imshow("Nail Detection Live", img)

        # cv2.waitKey(1)

        
    # closing the window
    cv2.destroyAllWindows()
    source.release()

    print(f'{count} fps')

def test02():

    # Start default camera
    video = cv2.VideoCapture(0);

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Number of frames to capture
    num_frames = 120;

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time()

    # Grab a few frames
    for i in range(0, num_frames) :
        ret, frame = video.read()

    # End time
    end = time()

    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))

    # Release video
    video.release()



def main():
    # get_fps()
    test02()



if __name__=='__main__':
    main()
    