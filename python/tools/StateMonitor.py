# coding=utf-8

import numpy as np
import cv2
import threading
import time
import matplotlib.pyplot as plt

class StateMonitor():
    data_size = 0
    top_site = []
    down_site = []
    middle_site = []
    times = []
    data_update = False
    data_height = 0
    lock = threading.Lock()

    @classmethod
    def __init__(self, height):
        self.data_height = height
        t = threading.Thread(target=self.imshowData)
        t.start()
        # t.join()
        
    @classmethod
    def monitor(self, top_x, top_y, down_x, down_y):
        self.lock.acquire()

        self.data_size += 1

        if top_y < 0:
            print ("top_y: ", top_y)

        if top_y < 0:
            print ("down_y: ", down_y)

        self.times.append(self.data_size)

        self.top_site.append(top_y)
        self.down_site.append(down_y)

        # shap = (down_y - top_y) / (down_x - top_x)
        # if shap < 1:
        #     self.middle_site.append(self.data_height - 50)
        # else:
        #     self.middle_site.append(50)
        self.middle_site.append(down_y-top_y)
        # print (self.data_size)
        # print ('monitor now...')
        self.data_update = True
        self.lock.release()

    @classmethod
    def imshowData(self):
        while True:
            if self.data_update:
                self.lock.acquire()
                # print ('imshow now...')
                self.drawData()
                self.data_update = False
                self.lock.release()
            else:
                time.sleep(1)

    @classmethod
    def drawData(self):
        plt.subplot(111)
        plt.cla()
        plt.title("state")
        plt.ylim(-10, self.data_height)
        plt.plot(self.times,self.top_site, 'b',label='top_site')
        plt.plot(self.times,self.down_site, 'g',label='down_site')
        plt.plot(self.times,self.middle_site, 'r',label='down_site-top_site')
        plt.legend()
        plt.pause(0.00001)