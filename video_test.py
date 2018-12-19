import numpy as np  
import sys,os  
import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('test.mp4')
    width = 1080
    height = 720
    sz = (1080, 720)
    fps = 1
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vout = cv2.VideoWriter('output.avi', fourcc, 20.0, sz, True)
    # for i in range (0, 10): 
    while(1):
        ret, img = cap.read()
        try:
            img.shape
        except:
            print ('finish')
            break
        back_img = np.zeros((720, 1080, 3), dtype=np.uint8)
        back_img.fill(0)
        # back_img2 = cv2.add(back_img, img)
        # back_img = img.new('RGB', (1080, 720), 'white')
        for w in range(img.shape[1]):
            for h in range(img.shape[0]):
                back_img[h, w] = img[h, w]
        print ('running...')
        # back_img = back_img + img
        back_img2 = cv2.flip(back_img, 1)
        vout.write(back_img)
    vout.release()