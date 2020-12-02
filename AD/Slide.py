from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Button import *

class Slide_Thickness(QWidget):
    """
    그림판에서 선굵기를 변경을 누르면 나타나는 창입니다. 슬라이드를 통해 크기를 변경할 수 있습니다.
    변화된 크기는 선/직선/지우개 개별적으로 저장됩니다.
    """
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

        self.setUI()

    # UI설정
    def setUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        #폰트설정
        font=QFont('Uroob',30)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(1,50)
        self.sld.setValue(self.currentsize)

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
        self.setFixedSize(200,120)
        self.move(300,300)
        self.setWindowTitle(self.title)
        self.show()

    # 바뀐 슬라이드 값을 표시하는 함수
    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    # 취소/확인 버튼 입력시
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

# 텍스트 바꾸기
class Slide_ChangedText(QWidget):
    """
    그림판에 텍스트를 입력하기 할 때 텍스트의 크기를 정하기 위한 창입니다.
     슬라이드를 통해 텍스트 크기를 변경할 수 있습니다.
    """
    def __init__(self, item, tool, items):
        super().__init__()
        self.title='폰트변경'
        self.item = item
        self.tool = tool
        self.items = items

        for r in range(0, len(items)):
            if self.item == self.items[r]:
                self.currentsize = self.tool.canvas.stringFontSize

        self.setUI()

    # UI설정
    def settUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        # 폰트설정
        font = QFont('Uroob', 30)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(1,50)
        self.sld.setValue(self.currentsize)

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
        self.setFixedSize(200,120)
        self.move(300,300)
        self.setWindowTitle(self.title)
        self.show()

    # 바뀐 슬라이드 값 표시 함수
    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    # 취소/확인 버튼 입력시
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

# 투명도바꾸기
class Slide_ColorEffect(QWidget):
    """
    그림판에서 선/직선/지우개의 투명도를 조절하는 창입니다.
    슬라이드를 통해 투명도를 조절할 수 있습니다.
    """
    def __init__(self, tool):
        super().__init__()
        self.title='색효과'
        self.tool = tool
        self.currentsize = self.tool.save_alpha

        self.settUI()

    # UI설정
    def setUI(self):
        # 위젯들 정의
        self.size = QLabel(str(self.currentsize))
        self.sld = QSlider(Qt.Horizontal, self)
        self.okbutton = Button('ok', self.buttonClicked)
        self.cancelbutton = Button('cancel', self.buttonClicked)

        # 위젯들 설정
        #폰트설정
        font=QFont('Uroob',30)
        self.size.setFont(font)
        # 슬라이드 설정
        self.sld.setFixedSize(180,20)
        self.sld.setRange(0, 255)
        self.sld.setValue(self.currentsize)

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
        self.setFixedSize(200,120)
        self.move(300,300)
        self.setWindowTitle('투명도 조절')
        self.show()

    # 바뀐 슬라이드 값을 표시하는 함수
    def setText(self):
        self.size.setText(str(self.sld.value()))
        self.currentsize = self.sld.value()

    # 취소/확인 버튼 입력시
    def buttonClicked(self):
        button = self.sender()
        if button.text() == 'ok':
            self.tool.save_alpha = self.currentsize
            self.tool.ChangedRGBA(self.tool.save_red, self.tool.save_green, self.tool.save_blue, self.tool.save_alpha)
            self.close()
        elif button.text() == 'cancel':
            self.close()

#########################################################
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = Slide_Thickness()
    sys.exit(app.exec_())
