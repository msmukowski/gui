import cv2 as cv
import numpy as np


class Target:
    def __init__(self) -> None:
        '''Initialize new Target class instance'''
        # camera settings
        self.run = True
        self.camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.key_cap = ord('s')
        # work images and its parameters
        self.image = self.camera.read()[1]
        self.result = self.image.copy()
        self.mask = self.image.copy()
        self.hsv = cv.cvtColor(self.image,cv.COLOR_BGR2HSV)
        self.width, self.height = self.image.shape[:2]
        # gui window parameters
        self.window_name = 'GUI'
        self.window = cv.namedWindow(self.window_name)
        # calibration trackbar
        self.calibrate, _ = 0, cv.createTrackbar('Calibrate', self.window_name,0,1,self.on_trackbar)
        cv.setTrackbarMin('Calibrate',self.window_name,0), cv.setTrackbarPos('Calibrate',self.window_name,0)
        # sensivity trackbar
        self.sensitivity, _ = 18, cv.createTrackbar('Sensitivity', self.window_name,0,40,self.on_trackbar)
        cv.setTrackbarMax('Sensitivity',self.window_name,40), cv.setTrackbarPos('Sensitivity',self.window_name,18)
        # other parameters
        self.target_min_area = 700

    def display(self, obj):
        cv.imshow(self.window_name, obj)
        self.key_cap = cv.waitKey(1)

    def edge_detection(self):
        '''Finds the outlines of objects in an image and draws them.
        According to its shape, it indicates whether it is round'''
        contours, _ = cv.findContours(self.mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv.contourArea(contour)

            if area > self.target_min_area:
                cv.drawContours(self.result, [contour], -1, (255, 0, 0), 2)
                peri = cv.arcLength(contour, True)
                approx = cv.approxPolyDP(contour, 0.02 * peri, True)
                x_, y_, w, h = cv.boundingRect(approx)
                cv.rectangle(self.result, (x_, y_), (x_ + w, y_ + h), (0, 255, 255), 2)
                ((x, y), radius) = cv.minEnclosingCircle(contour)

                circle_check = int(area) / int(np.pi * np.power(radius, 2))

                if circle_check > 0.8:
                    cv.putText(self.result, "CIRCLE", (x_ + int(w / 4), y_ + int(h / 2)), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                               (0, 153, 255), 2)

    def update(self):
        _, frame = self.camera.read()
        self.result = frame.copy()
        self.trackbar()
        self.green_mask(frame)
        self.edge_detection()
        self.info()

    def cleanup(self):
        self.run = False
        self.camera.release()
        cv.destroyAllWindows()

    def on_trackbar(self, value):
        pass

    def trackbar(self):
        if self.calibrate != 1:
            cv.setTrackbarPos('Sensitivity',self.window_name,self.sensitivity)
        else:
            self.sensitivity = cv.getTrackbarPos('Sensitivity', self.window_name)

        self.calibrate = cv.getTrackbarPos('Calibrate', self.window_name)

    def green_mask(self, obj):
        '''Creates green mask of an image'''
        blur = cv.GaussianBlur(obj, (5,5), 0)
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

        lower_green = np.array([68 - self.sensitivity, 100, 50])
        higher_green= np.array([68 + self.sensitivity, 255, 255])
        self.mask = cv.inRange(hsv, lower_green, higher_green)

    def info(self):
        '''Displays info on top of the interface'''
        cv.putText(self.result, "Press 'q' to exit", (int(self.width*0.93),int(self.height*0.73)),
                   cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)
