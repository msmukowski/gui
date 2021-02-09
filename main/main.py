from helpers import Target

obj = Target("sample.jpg")

obj.display(obj.edgeDetection(obj.grayscale))
