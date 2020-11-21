import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Canvas(QMainWindow):

    def __init__(self,painter):
        super().__init__()

        self.painter=painter

        self.image = QImage(QSize(725, 430), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False

        self.brush_color = Qt.black
        self.brush_size = 5

        #self.ChangedSize(5)
        self.last_point = QPoint()
        self.initUI()





    def initUI(self):

        #menubar = self.menuBar()
        #menubar.setNativeMenuBar(False)
        #filemenu = menubar.addMenu('File')



        #tools = ToolUI(self)
        #tools.tools[7].addAction(save_action)
        #tools.tools[8].addAction(clear_action)

        #filemenu.addAction(save_action)
        #filemenu.addAction(clear_action)

        self.setWindowTitle('Simple Painter')
        self.setGeometry(300, 300, 725, 430)
        self.show()

    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False





if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas()
    sys.exit(app.exec_())