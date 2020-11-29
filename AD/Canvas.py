import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Canvas(QMainWindow):

    def __init__(self, status):
        super().__init__()

        self.status = status

        self.drawingPath = None

        # 저장된 그림 불러오기/ 새로만들기
        self.image = QPixmap()
        filename="pictures/{}_main_image.png".format(self.status.playername)
        #해당 파일이름을 가진 그림이 존재하면,
        if os.path.isfile(filename):
            self.image.load(filename)
        else:
            mainImage = QImage(QSize(725, 430), QImage.Format_RGB32)
            mainImage.fill(Qt.white)
            mainImage.save(filename)
            self.image = QPixmap(filename)

        self.resize(self.image.width(),self.height())
        #####
        self.drawing = False

        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.color_a = 255
        self.brush_color = QColor(self.color_r, self.color_g, self.color_b, self.color_a)
        self.brush_size = 5
        self.brush_mode = Qt.SolidLine


        self.string = 'you and me'
        self.stringFont = 'DejaVu Sans Mono'
        self.stringFontSize = 18


       # 모드 선택 ['drawing':그리기, 'line':직선, 'text':텍스트, ]
        self.save_drawingType = 'drawing'


        # 직선 모드에서 활용할 point
        self.past_point = None
        self.present_point = None


        self.initUI()



    def initUI(self):
        self.setWindowTitle('Simple Painter')
        self.setGeometry(300, 300, 725, 430)
        self.show()


    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawPixmap(self.rect(), self.image, self.rect())
        if self.drawingPath:
            canvas.setPen(QPen(self.brush_color, self.brush_size, self.brush_mode, Qt.RoundCap))
            canvas.drawPath(self.drawingPath)


    # 좌클릭을 눌렀을 때
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawingPath = QPainterPath()
            self.drawingPath.moveTo(e.pos())
            if self.save_drawingType == 'drawing':
                pass
            else:
                self.past_point = e.pos()


    # 좌클릭을 한 상태로 움직일 때
    def mouseMoveEvent(self, e):
        if e.buttons() and Qt.LeftButton and self.drawingPath:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, self.brush_mode, Qt.RoundCap))
            if self.save_drawingType == 'text':
                pass
            else:
                self.drawingPath.lineTo(e.pos())
                self.update()


    # 좌클릭 버튼에서 손이 떼졌을 때
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.drawingPath:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, self.brush_mode, Qt.RoundCap))

            if self.save_drawingType == ('drawing'):
                painter.drawPath(self.drawingPath)
            elif self.save_drawingType == 'line':
                self.present_point = e.pos()
                painter.drawLine(self.past_point, self.present_point)
            elif self.save_drawingType == 'text':
                painter.setPen(self.brush_color)
                painter.setFont(QFont(self.stringFont, self.stringFontSize))
                painter.drawText(self.past_point, self.string)

            self.drawingPath = None
            self.update()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    canvas = Canvas('heng')
    sys.exit(app.exec_())
