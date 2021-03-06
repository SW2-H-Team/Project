from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Button import *



class Slide_Thickness(QWidget):
    def __init__(self, tool):
        super().__init__()

        self.tool = tool
        # 현재 사용중인 도구의 크기를 조절함.
        if self.tool.tools[0].isChecked():
            self.currentsize = self.tool.save_brush_size
            self.title = '브러쉬 크기 조절'
        elif self.tool.tools[1].isChecked():
            self.currentsize = self.tool.save_line_size
            self.title = '직선 굵기 조절'
        elif self.tool.tools[2].isChecked():
            self.currentsize = self.tool.save_eraser_size
            self.title = '지우개 크기 조절'

        self.initUI()

    def initUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        font=self.size.font()
        font.setPointSize(20)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(1,50)
        self.sld.setValue(self.currentsize)
        self.size = QLabel(str(self.sld.value()))

        self.okbutton.setFixedSize(80,30)
        self.cancelbutton.setFixedSize(80,30)

        self.sld.valueChanged.connect(self.setText)
        # 레이아웃
        mainlayout = QGridLayout()

        mainlayout.addWidget(self.size,0,5,1,5)
        mainlayout.addWidget(self.sld,2,0,2,5)
        mainlayout.addWidget(self.okbutton,3,3,4,5)
        mainlayout.addWidget(self.cancelbutton,3,0,4,2)

        self.setLayout(mainlayout)
        self.setFixedSize(200,100)
        self.move(300,300)
        self.setWindowTitle(self.title)
        self.show()

    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    def buttonClicked(self):
        button = self.sender()
        if button.text()=='ok':
            if self.tool.tools[0].isChecked():
                self.tool.save_brush_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_brush_size)
            elif self.tool.tools[1].isChecked():
                self.tool.save_line_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_line_size)
            elif self.tool.tools[2].isChecked():
                self.tool.save_eraser_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_eraser_size)
            self.close()
        elif button.text()=='cancel':
            self.close()








class Slide_ChangedText(QWidget):
    def __init__(self, item, tool, items):
        super().__init__()
        self.title='폰트변경'
        self.item = item
        self.tool = tool
        self.items = items

        for r in range(0, len(items)):
            if self.item == self.items[r]:
                self.currentsize = self.tool.canvas.stringFontSize



        self.initUI()

    def initUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        font=self.size.font()
        font.setPointSize(20)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(1,50)
        self.sld.setValue(self.currentsize)
        self.size = QLabel(str(self.sld.value()))

        self.okbutton.setFixedSize(80,30)
        self.cancelbutton.setFixedSize(80,30)

        self.sld.valueChanged.connect(self.setText)
        # 레이아웃
        mainlayout = QGridLayout()

        mainlayout.addWidget(self.size,0,5,1,5)
        mainlayout.addWidget(self.sld,2,0,2,5)
        mainlayout.addWidget(self.okbutton,3,3,4,5)
        mainlayout.addWidget(self.cancelbutton,3,0,4,2)

        self.setLayout(mainlayout)
        self.setFixedSize(200,100)
        self.move(300,300)
        self.setWindowTitle(self.title)
        self.show()

    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    def buttonClicked(self):
        button = self.sender()
        if button.text()=='ok':
            for r in range(0, len(self.items)):
                if self.item == self.items[r]:
                    self.tool.canvas.stringFont = self.items[r]
                    self.tool.ChangedFont(self.tool.canvas.stringFont, self.currentsize)
            self.close()
        elif button.text()=='cancel':
            self.close()








class Slide_ColorEffect(QWidget):
    def __init__(self, tool, status):
        super().__init__()
        self.title='색효과'
        self.tool = tool
        self.status = status
        #RGB값 저장
        self.save_red = self.status.a
        self.save_blue = self.status.b
        self.save_green = self.status.c
        self.save_alpha = 255
        self.save_brush_color = QColor(self.save_red, self.save_green, self.save_blue, self.save_alpha)
        #
        self.currentsize = self.save_alpha

        self.initUI()

    def initUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        font=self.size.font()
        font.setPointSize(20)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(0, 255)
        self.sld.setValue(self.currentsize)
        self.size = QLabel(str(self.sld.value()))

        self.okbutton.setFixedSize(80,30)
        self.cancelbutton.setFixedSize(80,30)

        self.sld.valueChanged.connect(self.setText)

        # 레이아웃
        mainlayout = QGridLayout()

        mainlayout.addWidget(self.size,0,5,1,5)
        mainlayout.addWidget(self.sld,2,0,2,5)
        mainlayout.addWidget(self.okbutton,3,3,4,5)
        mainlayout.addWidget(self.cancelbutton,3,0,4,2)

        self.setLayout(mainlayout)
        self.setFixedSize(200,100)
        self.move(300,300)
        self.setWindowTitle(self.title)
        self.show()

    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    def buttonClicked(self):
        button = self.sender()
        if button.text()=='ok':
<<<<<<< HEAD
            self.save_alpha = self.currentsize
            self.save_brush_color = QColor(self.save_red, self.save_green, self.save_blue, self.save_alpha)
            self.tool.ChangedColor(self.save_brush_color)
=======
            self.tool.save_alpha = self.currentsize
            self.tool.ChangedRGBA(self.tool.save_red, self.tool.save_green, self.tool.save_blue, self.tool.save_alpha)
>>>>>>> 625c7a117911d74d6a01223e2494f191b876b406
            self.close()
        elif button.text()=='cancel':
            self.close()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Slide_Thickness()
    sys.exit(app.exec_())
