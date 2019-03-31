# --*-- encoding: utf-8 --*--

import cv2
# import argparse
import numpy as np
from optparse import OptionParser #用来在命令行添加选项
import multiprocessing
import time

def gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换成灰度图

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--Input","-i",  dest="video_path", help="Path to input_video.")  # 输入文件
    parser.add_option("--Output","-o",  dest="out_video_path",default='output.avi', help="Path to output_video.")  # 输出文件
    parser.add_option('--parallel', type=int, default=1, help='number of threads/processes to run')  # 并行数目
    (options, args) = parser.parse_args()

    if not options.video_path:  # if filename is not given
        parser.error('Error: path to video must be specified. Pass --Input to command line')

    pool = multiprocessing.Pool(processes=options.parallel)  # 创建n个进程
    video_full_path = options.video_path
    cap = cv2.VideoCapture(video_full_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 获取cap视频流的每帧大小
    # 定义编码格式
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    outVideo = cv2.VideoWriter(options.out_video_path, fourcc, fps, size, isColor=False)

    frame_count = 1
    success = True
    print('Generating video file...')
    start = time.time()
    while (success):
        success, frame = cap.read()  # 读取一个帧
        if not success:  # 读到视频结尾
            break
        image = pool.apply_async(gray, (frame,)).get()
        outVideo.write(image)
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程
    pool.join()  # 等待进程池中的所有进程执行完毕
    done = time.time()
    print('Time：%d s' % (done - start))
