#coding = utf-8
import cv2
import os
import glob as gb
from optparse import OptionParser #用来在命令行添加选项
import time

def color_video_to_gray_video(path,out_path):

    video_capture = cv2.VideoCapture()
    video_capture.open(path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    num_frame = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, size ,0)

    print('Source file path：%s' % path)
    print('Generating video file, generating path：%s'%out_path)
    ret, frame = video_capture.read()
    while ret:
        video_writer.write(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
        ret, frame = video_capture.read()
    print('DONE')

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--Input","-i",  dest="video_path", help="Path to input_video.")
    parser.add_option("--Output","-o",  dest="out_video_path",default='output.avi', help="Path to output_video.")
    (options, args) = parser.parse_args()
    # print(options.video_path)

    if not options.video_path:  # if filename is not given
        parser.error('Error: path to video must be specified. Pass --Input to command line')

    try:
        start = time.time()
        color_video_to_gray_video(options.video_path,options.out_video_path)
        done = time.time()
        print('Time：%dS' % (done - start))
    except Exception as e:
        print('Exception: {}'.format(e),'\n','Example:>python main.py --Input video_path  --Output  video_output_path')



