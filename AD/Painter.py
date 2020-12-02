from PyQt5.QtWidgets import *

import Canvas
import PainterTool

#그림판
class Painter(QWidget):
    """
    그림판입니다. 그림을 그릴 수 있는 캔버스와 그리기 설정을 할 수 있는 도구레이어로 나뉩니다.
    """

    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status
        self.setGeometry(300, 300, 750, 510)
        self.setUI()

    # UI설정
    def setUI(self):
        ###레이아웃
        mainlayout = QGridLayout()
        toollayout = QHBoxLayout()
        canvaslayout = QGridLayout()

        mainlayout.addLayout(toollayout, 0, 0, 1, 10)
        mainlayout.addLayout(canvaslayout, 1, 0, 9, 10)
        self.setLayout(mainlayout)

        #캔버스
        self.canvas = Canvas.Canvas(self.status)
        canvaslayout.addWidget(self.canvas)

        #도구
        tools = PainterTool.ToolUI(self.canvas,self.status)
        toollayout.addWidget(tools)

#########################################################
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    painter = Painter()
    painter.show()
    sys.exit(app.exec_())
