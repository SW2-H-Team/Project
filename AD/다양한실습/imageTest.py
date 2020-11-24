from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas():

    def __init__(self):
        super().__init__()
        self.mainImage = QImage(QSize(725, 430), QImage.Format_RGB32)
        self.mainImage.fill(Qt.white)
        self.mainImage.save("/home/user/main_image.png")



if __name__ == "__main__":
    Canvas()
