from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


from Button import *


class Slide_Thickness(QWidget):
    def __init__(self,item,tool, items):
        super().__init__()
        self.title='굵기변경'
        self.item = item
        self.tool =tool
        self.items = items

        if self.item == self.items[0]:
            self.currentsize = self.tool.save_brush_size
        elif self.item == self.items[1]:
            self.currentsize = self.tool.save_line_size
        elif self.item == self.items[2]:
            self.currentsize = self.tool.save_eraser_size

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
            if self.item == self.items[0]:
                self.tool.save_brush_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_brush_size)
            elif self.item == self.items[1]:
                self.tool.save_line_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_line_size)
            elif self.item == self.items[2]:
                self.tool.save_eraser_size = self.currentsize
                self.tool.ChangedSize(self.tool.save_eraser_size)
            self.close()
        elif button.text()=='cancel':
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Slide()
    sys.exit(app.exec_())
