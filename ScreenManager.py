import cv2
import numpy as np

class CheckImage:

    def __init__(self):
        self.image = None
        self.grey = None
        self.width = 0
        self.height = 0

    def upload_image(self, image):
        try:
            #self.image = cv2.imread(image)
            data = np.fromstring(image, dtype=np.uint8)
            self.image = cv2.imdecode(data, 1)
            self.grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        except IOError:
            pass

    def find_image(self, image):
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(self.grey, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.75
        loc = np.where(res >= threshold)
        try:
            pt = (loc[1][0]+w/2, loc[0][0]+h/2)
            return pt
        except IndexError:
            return ()
