import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Canvas(QMainWindow):

    def __init__(self, painter):
        super().__init__()

        self.painter = painter

        self.image = QImage(QSize(725, 430), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False

        self.brush_color = QColor(0, 0, 0)
        self.brush_size = 5
        self.brush_mode = Qt.SolidLine

        self.string = 'you and me'
        self.stringFont = 'DejaVu Sans Mono'
        self.stringFontSize = 18


       # 모드 선택 ['drawing':그리기, 'line':직선, 'text':텍스트]
        self.save_drawingType = 'drawing'


        # 직선 모드에서 활용할 point
        self.past_point = QPoint()
        self.present_point = QPoint()

        # 그리기 모드에서 활용할 point
        self.last_point = QPoint()


        self.initUI()





    def initUI(self):
        self.setWindowTitle('Simple Painter')
        self.setGeometry(300, 300, 725, 430)
        self.show()


    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())


    # 좌클릭을 눌렀을 때
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.save_drawingType == 'drawing':
                self.drawing = True
                self.last_point = e.pos()
            elif self.save_drawingType == 'line':
                self.drawing = True
                self.past_point = e.pos()
            elif self.save_drawingType == 'text':
                self.drawing = True
                self.last_point = e.pos()


    # 좌클릭을 한 상태로 움직일 때
    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, self.brush_mode, Qt.RoundCap))

            if self.save_drawingType == 'drawing':
                painter.drawLine(self.last_point, e.pos())
                self.last_point = e.pos()
            elif self.save_drawingType == 'line':
                if self.brush_size <= 3:
                    painter.setPen(QPen(Qt.gray, 1))
                else:
                    painter.setPen(QPen(Qt.gray, self.brush_size // 3, self.brush_mode, Qt.RoundCap))
                painter.drawPoint(self.past_point)
            elif self.save_drawingType == 'text':
                pass

            self.update()


    # 좌클릭 버튼에서 손이 떼졌을 때
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.save_drawingType == 'drawing':
                self.drawing = False
            elif self.save_drawingType == 'line':
                painter = QPainter(self.image)
                painter.setPen(QPen(self.brush_color, self.brush_size, self.brush_mode, Qt.RoundCap))
                self.present_point = e.pos()
                painter.drawLine(self.past_point, self.present_point)
                self.update()
                self.drawing = False
            elif self.save_drawingType == 'text':
                painter = QPainter(self.image)
                self.draw_text(painter)
                self.drawing = False



    def draw_text(self, qp):
        qp.setFont(QFont(self.stringFont, self.stringFontSize))
        qp.drawText(self.last_point, self.string)
        self.update()





if __name__ == '__main__':

    app = QApplication(sys.argv)
    canvas = Canvas('heng')
    sys.exit(app.exec_())
