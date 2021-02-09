import cv2 as cv
import numpy as np


class Target:
    def __init__(self, image_path) -> None:
        self.image_path = ""
        self.image = cv.imread(image_path)
        self.grayscale = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY)
        self.window_name = 'Task'
        self.window = cv.namedWindow(self.window_name)

    def display(self, obj):
        cv.imshow(self.window_name, obj)
        cv.waitKey(0)

    def edgeDetection(self,obj):
        threshold = cv.adaptiveThreshold(obj,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,155,1)
        kernel_opening = np.ones((15, 15), np.float32)
        kernel_closure = np.ones((3, 3), np.float32)
        opening = cv.morphologyEx(threshold,cv.MORPH_OPEN, kernel_opening)
        blur = cv.bilateralFilter(opening, 19, 75, 75)
        closure = cv.morphologyEx(blur,cv.MORPH_CLOSE, kernel_closure)
        edges = cv.Canny(closure, 50, 150)

        return edges
