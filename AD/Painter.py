from PyQt5.QtWidgets import *

import Canvas
import PainterTool

class Painter(QWidget):

    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status
        self.setGeometry(300, 300, 750, 510)
        self.setUI()

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
        tools = PainterTool.ToolUI(canvas,self.status)
        toollayout.addWidget(tools)


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
