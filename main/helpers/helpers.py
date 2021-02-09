import cv2 as cv
import numpy as np


class Target:
    def __init__(self) -> None:
        self.run = True
        self.camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.key_cap = ord('s')
        self.image = self.camera.read()[1]
        self.result = self.image.copy()
        self.grayscale = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY)
        self.width, self.height = self.grayscale.shape
        self.window_name = 'GUI'
        self.window = cv.namedWindow(self.window_name)
        self.calibrate, _ = 0, cv.createTrackbar('Calibrate', self.window_name,0,1,self.on_trackbar)
        cv.setTrackbarMin('Calibrate',self.window_name,0), cv.setTrackbarPos('Calibrate',self.window_name,0)
        self.tb_thresh, _ = 11, cv.createTrackbar('Threshold', self.window_name,0,255,self.on_trackbar)
        cv.setTrackbarMin('Threshold',self.window_name,1), cv.setTrackbarPos('Threshold',self.window_name,1)
        self.edges = np.zeros((self.width, self.height,1), np.uint8)

    def display(self, obj):
        cv.imshow(self.window_name, obj)
        self.key_cap = cv.waitKey(1)

    def edge_detection(self, obj):
        kernel_opening = np.ones((3, 3), np.float32)
        kernel_closure = np.ones((3,3), np.float32)
        blur = cv.bilateralFilter(obj, 10, 50, 50)
        blur = cv.medianBlur(blur,5)
        #threshold = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,1+2*self.tb_thresh,1)
        opening = cv.morphologyEx(blur,cv.MORPH_OPEN, kernel_opening)
        closure = cv.morphologyEx(opening,cv.MORPH_CLOSE, kernel_closure)
        self.edges = cv.Canny(blur, 10, 50)

    def contours_detection(self):
        contours, hierarchy = cv.findContours(self.edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            #epsilon = 0.31 * cv.arcLength(contour, True)
            #approx = cv.approxPolyDP(contour, epsilon, True)
            cv.drawContours(self.result, contour, -1,(21,0,255),-1)

    def update(self):
        _, frame = self.camera.read()
        self.result = frame.copy()
        self.grayscale = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        self.trackbar()
        self.edge_detection(self.grayscale)
        self.contours_detection()
        self.display(self.result)

    def cleanup(self):
        self.run = False
        self.camera.release()
        cv.destroyAllWindows()

    def on_trackbar(self, value):
        pass

    def trackbar(self):
        if self.calibrate != 1:
            cv.setTrackbarPos('Threshold',self.window_name,self.tb_thresh)
        else:
            self.tb_thresh = cv.getTrackbarPos('Threshold', self.window_name)

        self.calibrate = cv.getTrackbarPos('Calibrate', self.window_name)

