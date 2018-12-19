import numpy as np  
import sys,os  
import cv2
caffe_root = '/home/wxx/develop/caffe-ssd/'
sys.path.insert(0, caffe_root + 'python')  
import caffe
import shutil
import time

caffe.set_mode_gpu()

net_file= '../example/MobileNetSSD_deploy.prototxt'  
caffe_model='../snapshot/r/mobilenet_iter_28000.caffemodel'  
test_dir = "images"

if not os.path.exists(caffe_model):
    print(caffe_model + " does not exist")
    exit()
if not os.path.exists(net_file):
    print(net_file + " does not exist")
    exit()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

CLASSES = ('background','person','test')

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
    img = preprocess(origimg)
    
    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()
    start_time = time.time()
    box, conf, cls = postprocess(origimg, out)
    # if len(box) <= 0:
    #     return -5
    for i in range(len(box)):
        p1 = (box[i][0], box[i][1])
        p2 = (box[i][2], box[i][3])
        print (p1)
        print (p2)
        # if box[i][0] <=0 or box[i][1] <= 0 or box[i][2] <= 0 or box[i][3] <= 0:
        #     return -4
        # site = 
        if int(cls[i]) == 1:
            cv2.rectangle(origimg, p1, p2, (0,255,255))
        elif int(cls[i]) > 1:
            break
        else:
            cv2.rectangle(origimg, p1, p2, (255,0,0))
        p3 = (max(p1[0], 15), max(p1[1], 15))
        title = "%s:%.2f:%d" % (CLASSES[int(cls[i])], conf[i],i)
        cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (255, 0, 0), 1)
        if int(cls[i]) == 1:
            result = 1

    cv2.imshow("SSD", origimg)
    k = cv2.waitKey(1) & 0xff

    # k = cv2.waitKey(0) & 0xff
        #Exit if ESC pressed
    if k == 27 : result = -1
    return result

######## video  ##############
if __name__ == '__main__':
    cap = cv2.VideoCapture('/home/wxx/develop/demo4/video/walk2/test39.mp4')
    while(1): 
        ret, img = cap.read()
        detect(img)

######## img  ##############
# if __name__ == '__main__':
#     img = cv2.imread("/home/wxx/testimg/02563.jpg")
#     witch = detect(img)

######## photo_test ##############
# if __name__ == '__main__':
#     imgpath = '/home/wxx/testimg/'
#     witch = 0
#     for i1 in range(0,9):
#         if witch == -1:
#             break
#         for i2 in range(0,9):
#             if witch == -1:
#                 break
#             for i3 in range(0,9):
#                 if witch == -1:
#                     break
#                 for i4 in range(0,9):
#                     imgname = '0' + str(i1) + str(i2) + str(i3) + str(i4) + '.jpg'
#                     imgfile = imgpath + imgname
#                     img = cv2.imread(imgfile)
#                     try:
#                         img.shape
#                         witch = detect(img)
#                     except:
#                         print('fail to read '+imgfile)
#                         continue

######## photo_result  ##############
# if __name__ == '__main__':
#     imgpath = '/home/wxx/img/person_data/JPEGImages/'
#     witch = 0
#     width = 1080
#     height = 720
#     sz = (width, height)
#     fps = 1
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     vout = cv2.VideoWriter('output.avi', fourcc, 20.0, sz, True)
#     back_img = np.zeros((720, 1080, 3), dtype=np.uint8)
#     # vout.open()
#     for i1 in range(0,9):
#         if witch == -1:
#             break
#         for i2 in range(0,9):
#             if witch == -1:
#                 break
#             for i3 in range(0,9):
#                 if witch == -1:
#                     break
#                 for i4 in range(0,9):
#                     imgname = '0' + str(i1) + str(i2) + str(i3) + str(i4) + '.jpg'
#                     imgfile = imgpath + imgname
#                     img = cv2.imread(imgfile)
#                     try:
#                         img.shape
#                         witch = detect(img)
#                         # back_img.fill(0)
#                         # for w in range(img.shape[1]):
#                         #     for h in range(img.shape[0]):
#                         #         back_img[h, w] = img[h, w]
#                         # vout.write(back_img)
#                         # pirnt('running')
#                         cv2.imwrite('result/'+imgname, img)
#                     except:
#                         print('fail to read '+imgfile)
#                         continue
#     vout.release()

######## copy  ##############
# if __name__ == '__main__':
#     imgpath = '/media/wxx/系统公用/add_data/'
#     witch = 0
#     print ('ok')
#     for i1 in range(0,9):
#         if witch == -1:
#             break
#         for i2 in range(0,9):
#             if witch == -1:
#                 break
#             for i3 in range(0,9):
#                 if witch == -1:
#                     break
#                 for i4 in range(0,9):
#                     imgname = '0' + str(i1) + str(i2) + str(i3) + str(i4) + '.jpg'

#                     imgfile = imgpath + imgname
#                     img = cv2.imread(imgfile)
#                     try:
#                         img.shape
#                         witch = detect(img)
#                         if witch == -4 or witch == -5:
#                             newname = '/home/wxx/testimg/' + imgname
#                             shutil.copyfile(imgfile,newname)
#                         elif witch == -1:
#                             break
#                     except:
#                         print('fail to read '+imgfile)
#                         continue
