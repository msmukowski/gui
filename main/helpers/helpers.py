import cv2 as cv


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