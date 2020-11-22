from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button
import Canvas
import ToolUI

class Painter(QWidget):

    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status
        self.setGeometry(300, 300, 750, 510)
        self.setUI()

        #self.currentcolor= Qt.black
        #self.currentsize=5

    def setUI(self):
        ###레이아웃
        mainlayout = QGridLayout()
        toollayout = QHBoxLayout()
        canvaslayout = QGridLayout()

        mainlayout.addLayout(toollayout, 0, 0, 1, 10)
        mainlayout.addLayout(canvaslayout, 1, 0, 9, 10)
        self.setLayout(mainlayout)

        #캔버스
        canvas = Canvas.Canvas(self.status)
        canvaslayout.addWidget(canvas)

        ## 툴
        #도구
        tools = ToolUI.ToolUI(canvas,self.status)
        toollayout.addWidget(tools)
        #tools = [ Button('{}'.format(str(x)),self.buttonClicked) for x in range(9)]
        #for i in range(len(tools)):
        #    toollayout.addWidget(tools[i])
        #toollayout.addStretch()


        #색상
        #toollayout.addWidget(QLabel('전경색: '))
        #toollayout.addWidget(Button('1',self.buttonClicked))
        #toollayout.addWidget(QLabel('배경색: '))
        #toollayout.addWidget(Button('2',self.buttonClicked))

    def buttonClicked(self):

        button = self.sender()
        key = button.text()
        print(key)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    painter = Painter()
    painter.show()
    sys.exit(app.exec_())
