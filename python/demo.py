import numpy as np  
import sys,os 
import cv2 
import shutil
import time

caffe_root = '/home/wxx/develop/caffe-ssd/'
sys.path.insert(0, caffe_root + 'python') 
import caffe
from StateJudge import StateJudge as state_judge

caffe.set_mode_gpu()

net_file= '../example/MobileNetSSD_deploy.prototxt'  
caffe_model='../snapshot/r1/mobilenet_iter_10000.caffemodel'  
test_dir = "images"

if not os.path.exists(caffe_model):
    print(caffe_model + " does not exist")
    exit()
if not os.path.exists(net_file):
    print(net_file + " does not exist")
    exit()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

CLASSES = ('background','person')

def preprocess(src):
    img = cv2.resize(src, (300,300))
    img = img - 127.5
    img = img * 0.007843
    return img

def postprocess(img, out):   
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0,0,:,3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0,0,:,1]
    conf = out['detection_out'][0,0,:,2]
    return (box.astype(np.int32), conf, cls)

def detect(origimg):
    result = 0
    img = preprocess(origimg)   # resize
    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()
    box, conf, cls = postprocess(origimg, out)

    optimal_obj = 0

    detect_num = len(box)
    if detect_num == 0:
        result = -3
    else:
        max_conf = conf[0]
        if detect_num > 1:
            for i in range(1, len(box)):
                if conf[i] > max_conf:
                    max_conf = conf[i]
                    optimal_obj = i

    if result != -3:
        if box[optimal_obj][1] < 0 or box[ optimal_obj][3] < 0:
            result = -2
        else:
            p1 = (box[optimal_obj][0], box[optimal_obj][1])
            p2 = (box[optimal_obj][2], box[optimal_obj][3])
            site = box[optimal_obj][1]
            state = state_judge.judge(box[optimal_obj][0], box[optimal_obj][1], box[optimal_obj][2], box[optimal_obj][3], img.shape[0])    # state judge))
            if state == -1:
                cv2.rectangle(origimg, p1, p2, (0,255,255))
            else:
                cv2.rectangle(origimg, p1, p2, (255,0,0))
            p3 = (max(p1[0], 15), max(p1[1], 15))
            title = "%s:%.2f" % (CLASSES[int(cls[optimal_obj])], conf[optimal_obj])
            cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 0, 0), 1)

    cv2.imshow("SSD", origimg)
    k = cv2.waitKey(1) & 0xff    #Exit if ESC pressed

    if k == 27 : result = -1
    return result

####### video  ##############
if __name__ == '__main__':
    # cap = cv2.VideoCapture('../video/test5.mp4')  ## 2
    cap = cv2.VideoCapture('../video/walking/test12.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    state_judge.setFPS(fps/3)
    # detect_faile = 1774
    # times = 0
    n = 0
    while(1): 
        ret, img = cap.read()
        n += 1
        if n >= 0:
            result = detect(img)
            n = 0
            if result == -1:
                break
    cv2.waitKey(0)
        # if result == -3 or result == -2:
        #     times += 1
        #     if times >= 5:
        #         cv2.imwrite('../detector_faile/0'+str(detect_faile)+'.jpg', img)
        #         detect_faile += 1
        #         times = 0

####### video_result  ##############
# if __name__ == '__main__':
#     cap = cv2.VideoCapture('../video/test3.mp4')
#     width = 1920
#     height = 1080
#     sz = (width, height)
#     fps = 1
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     vout = cv2.VideoWriter('output4.avi', fourcc, 20.0, sz, True)
#     back_img = np.zeros((height, width, 3), dtype=np.uint8)
#     while(1): 
#         ret, img = cap.read()
#         try:
#             img.shape
#         except:
#             break

#         try:
#             detect(img)
#             back_img.fill(0)
#             for w in range(img.shape[1]):
#                 for h in range(img.shape[0]):
#                     back_img[h, w] = img[h, w]
#             vout.write(back_img)
#         except:
#             continue
#     vout.release()
