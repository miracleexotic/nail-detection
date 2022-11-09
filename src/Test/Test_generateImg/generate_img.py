from math import ceil
import numpy as np
from PIL import Image
import pathlib
import moviepy.video.io.ImageSequenceClip

from matplotlib import pyplot as plt

# img size
WIDTH = 500
HEIGHT = 500

# path
path_to_base = pathlib.Path(__file__).parent / "base"
path_to_vdo = pathlib.Path(__file__).parent / "vdo"

def gen_img():
    """สร้างรูปภาพโดยไล่ตั้งแต่ 0-255 เป็นจำนวน 256 frame"""
    for i in range(256):
        print(f"{i}", end="")
        array = np.zeros([WIDTH, HEIGHT, 3], dtype=np.uint8)
        array[:,:] = [i, i, i]

        img = Image.fromarray(array)
        img.save(f'{path_to_base / "256"}\{i}.png')
        print(" - success")

def gen_vdo():
    """สร้างวิดีโอโดยมี frame ตั้งแต่ 0-255 -> 31 วินาที 1 ลูกคลื่น"""
    fps = 20
    path_to_256 = path_to_base / "256"
    delay_frame = [str(path_to_256 / "0.png") for i in range(20*3)] # delay 5 วิ ช่วงต้น-ท้าย
    start_frame = [str(path_to_256 / f"{i}.png") for i in range(256)] # คลื่นครึ่งแรก
    end_frame = [str(path_to_256 / f"{i}.png") for i in range(255, -1, -1)] # คลื่นครึ่งหลัง

    image_files = [*delay_frame, *start_frame, *end_frame, *delay_frame] # รวมทุก frame

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(f'{path_to_vdo}\output-256.mp4')

def gen_100_img():
    """สร้างรูปภาพโดยไล่ตั้งแต่ 0-255 เป็นจำนวน 100 frame"""
    rgb = 0
    count = 1
    while count <= 100:
        print(f"{count}:{ceil(rgb)}:{rgb}", end="")
        array = np.zeros([WIDTH, HEIGHT, 3], dtype=np.uint8)
        array[:,:] = [ceil(rgb), ceil(rgb), ceil(rgb)]

        img = Image.fromarray(array)
        img.save(f'{path_to_base / "100"}\{count}.png')
        print(" - success")
        count += 1
        rgb += 2.57

def gen_100_vdo():
    """สร้างวิดีโอโดยมี frame ตั้งแต่ 0-255 -> 40 วินาที 3 ลูกคลื่น"""
    fps = 20
    path_to_100 = path_to_base / "100"
    delay_frame = [str(path_to_100 / "1.png") for i in range(20*5)] # delay 5 วิ ช่วงต้น-ท้าย
    start_frame = [str(path_to_100 / f"{i}.png") for i in range(1, 101)] # คลื่นครึ่งแรก 
    # end_frame = [str(path_to_100 / f"{i}.png") for i in range(100, 0, -1)]
    end_frame = start_frame[::-1] # คลื่นครึ่งหลัง

    wave = [*start_frame, *end_frame] # คลื่น 1 ลูก
    wave3 = [*wave, *wave, *wave] # คลื่น 3 ลูก

    image_files = [*delay_frame, *wave3, *delay_frame] # รวมทุก frame

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(f'{path_to_vdo}\output-100.mp4')

def plot():
    start_delay_frame = [1 for i in range(20*5)]

    start_frame = []
    rgb = 0
    count = 1
    while count <= 100:
        start_frame.append(ceil(rgb))
        count += 1
        rgb += 2.57

    # start_frame = [i for i in range(1, 101)]
    end_frame = start_frame[::-1]
    end_delay_frame = [1 for i in range(20*5)]

    time_start_delay = []
    time_start = []
    time_end = []
    time_end_delay = []

    time_step = 0
    count = 0
    while time_step <= 20:
        if time_step <= 5:
            time_start_delay.append(time_step)
        elif time_step <= 10:
            time_start.append(time_step)
        elif time_step <= 15:
            time_end.append(time_step)
        else:
            time_end_delay.append(time_step)
        time_step += 0.05

    plt.plot([*time_start_delay, *time_start, *time_end, *time_end_delay], [*start_delay_frame, *start_frame, *end_frame, *end_delay_frame])
    plt.show()


if __name__ == '__main__':
    # gen_img()
    # gen_100_frame()
    # gen_vdo()
    # gen_100_vdo()
    plot()




