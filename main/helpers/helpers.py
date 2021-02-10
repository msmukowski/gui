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
        self.sensitivity = 0

    def display(self, obj):
        cv.imshow(self.window_name, obj)
        self.key_cap = cv.waitKey(1)

    def edge_detection(self, obj):
        kernel_opening = np.ones((15, 15), np.float32)
        kernel_closure = np.ones((3,3), np.float32)
        #blur = cv.bilateralFilter(obj, 16, 75, 75)
        #blur = cv.medianBlur(blur,15)
        blur = cv.GaussianBlur(obj,(9,9),1.5)
        #threshold = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,1+2*self.tb_thresh,2)
        #opening = cv.morphologyEx(blur,cv.MORPH_OPEN, kernel_opening)
        #closure = cv.morphologyEx(opening,cv.MORPH_CLOSE, kernel_closure)
        #dilate = cv.dilate(blur,kernel_closure)
        self.edges = cv.Canny(blur, 0, 50, 3)
        #self.edges = cv.dilate(self.edges,kernel_closure)

    def contours_detection(self):
        contours, hierarchy = cv.findContours(self.edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        for contour in contours:
            #epsilon = 0.31 * cv.arcLength(contour, True)
            #approx = cv.approxPolyDP(contour, epsilon, True)
            hull =cv.convexHull(contour)
            if cv.contourArea(contour) > 400:
                cv.drawContours(self.result, contour, -1,(0,0,255),thickness=6)
                print(f'Contour area: {cv.contourArea(contour)}')

    def update(self):
        _, frame = self.camera.read()
        self.result = frame.copy()
        self.grayscale = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        self.trackbar()
        self.edge_detection(self.grayscale)
        self.contours_detection()
        #self.display(self.edges)
        self.green(frame)
        self.display(np.concatenate((self.result,cv.cvtColor(self.edges,cv.COLOR_GRAY2BGR)), axis=1))

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
            self.sensitivity = self.tb_thresh

        self.calibrate = cv.getTrackbarPos('Calibrate', self.window_name)

    def green(self, obj):
        blur = cv.GaussianBlur(obj, (5,5), 0)
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

        lower_green = np.array([60 - self.sensitivity, 100, 100])
        higher_green= np.array([60 + self.sensitivity, 255, 255])
        mask = cv.inRange(hsv, lower_green, higher_green)

        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv.contourArea(contour)

            if area > 100:
                cv.drawContours(self.result, [contour], -1, (255,0,0), -1)