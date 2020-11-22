from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Button import Button
from Slide import *


class ToolUI(QWidget):
    def __init__(self, canvas, status, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.status = status
        self.save_eraser_size = 5
        self.save_brush_size = 5
        self.save_line_size = 5
        self.save_brush_mode = Qt.SolidLine
        self.save_brush_color = QColor(0, 0, 0)
        self.save_point = 5
        self.save_alpha = 255
        self.tool()

    def tool(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        # self.tools = [Button('{}'.format(str(x)), self.buttonClicked) for x in range(2)]
        self.tools = []

        self.tools.append(Button('그리기', self.buttonClicked))
        self.tools.append(Button('직선', self.buttonClicked))
        self.tools.append(Button('선굵기', self.buttonClicked))
        self.tools.append(Button('선모드', self.buttonClicked))
        self.tools.append(Button('색효과', self.buttonClicked))
        self.tools.append(Button('텍스트', self.buttonClicked))
        self.tools.append(Button('지우개', self.buttonClicked))

        self.tools.append(Button('저장', self.save))
        self.tools.append(Button('지우기', self.clear))

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)

        for i in range(len(self.tools)):
            layout.addWidget(self.tools[i])
        layout.addStretch()

        # 색상
        layout.addWidget(QLabel('색 바꾸기: '))
        # layout.addWidget(Button('1', self.foregroundColor()))
        # layout.addWidget(QLabel('배경색: '))
        # layout.addWidget(Button('배경', self.buttonClicked()))
        # layout.addWidget(QLabel('현재 색깔: '))

        # 색상 선택
        cb = QComboBox(self)
        self.status.cb = cb
        self.status.cb.addItem("Black")
        layout.addWidget(cb)

        self.status.cb.currentIndexChanged.connect(self.comboBoxFunction)

    # canvas로 전달
    def comboBoxFunction(self):
        self.save_brush_color = self.status.save_brush_color[self.status.cb.currentText()]
        self.ChangedColor(self.save_brush_color)


    # ------------------------------------------------------------------------ #


    # 그림 저장하기
    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                               "PNG(*.png);;JPEG(*.jpg);;JPEG(*.jpeg);;All Files(*.*) ")

        # 확장자명 구하기
        if _ == 'PNG(*.png)':
            _ = '.png'
        elif _ == 'JPEG(*.jpg)':
            _ = '.jpg'
        elif _ == 'JPEG(*.jpeg)':
            _ = '.jpeg'
        else:
            filenameExtension = fpath.find('.')
            filenameExtensionLen = len(fpath)
            _ = fpath[filenameExtension:filenameExtensionLen]
            fpath = fpath[0:filenameExtension]

        # 파일 저장하기
        if fpath:
            self.canvas.image.save(fpath + _)


    # 그림 초기화
    def clear(self):
        self.canvas.image.fill(Qt.white)
        self.canvas.update()

    # def foregroundColor(self):
    #    self.ChangedColor(Qt.red)

    # 배경색 (바뀌게 될지도 모르니까 그냥 냅둠)
    # def backgroungColor(self):
    #    self.ChangedColor(QColor(255,255,255))


    # 색깔과 사이즈에 변화주는 함수
    def ChangedColor(self, color):
        self.canvas.brush_color = color

    def ChangedSize(self, size):
        self.canvas.brush_size = size

    def ChangedValue(self, color, size):
        self.ChangedColor(color)
        self.ChangedSize(size)

    def ChangedFont(self, font, size):
        self.canvas.stringFont = font
        self.canvas.stringFontSize = size


    # ----------------------------------------------------------------------- #


    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '그리기':
            self.canvas.save_drawingType = 'drawing'
            self.ChangedValue(self.save_brush_color, self.save_brush_size)

        elif key == '지우개':
            self.canvas.save_drawingType = 'drawing'
            self.ChangedValue(QColor(255, 255, 255), self.save_eraser_size)

        elif key == '직선':
            self.canvas.save_drawingType = 'line'
            self.ChangedValue(self.save_brush_color, self.save_line_size)

        elif key == '선모드':
            self.save_brush_mode = self.changingMode()
            self.canvas.brush_mode = self.save_brush_mode
            self.ChangedValue(self.save_brush_color, self.save_brush_size)

        elif key == '선굵기':
            self.Thickness()

        elif key == '색효과':
            self.ColorEffect()

        elif key == '텍스트':
            self.canvas.save_drawingType = 'text'
            self.ChangedText()


    # 굵기 정하는 창 띄워주는 함수
    def Thickness(self):  # (원하는 굵기 종류, 굵기의 최대 범위, cancel 시 반환할 값)

        # 어떤 굵기를 바꿀 것인지
        items = ("그리기", "직선", "지우개")
        item, ok = QInputDialog.getItem(self, "선굵기", "변경하고 싶은 모드를 골라주세요.", items)

        if ok:
            self.sld = Slide_Thickness(item, self, items)


    # 변경할 것인지 물어보는 창 띄워주는 함수
    def changingMode(self):
        # 어떤 모드를 선택할 것인 것인지
        items = ("실선", "점선")
        list = [Qt.SolidLine, Qt.DotLine, ]
        result = self.save_brush_mode

        item, ok = QInputDialog.getItem(self, "선모드", "바꾸고자 하는 모드를 골라주세요.", items)

        if ok == False:
            pass
        else:
            if item == items[0]:
                result = list[0]
            else:
                result = list[1]

        return result


    # 텍스트 기능 실행을 위한 함수
    def ChangedText(self):
        s, OK = QInputDialog.getText(self, "입력글자", "텍스트에 입력할 글자를 적어주세요.")
        if OK:
            self.canvas.string = s
            items = ('Default', 'Arial', 'Times New Ronam', "Consolas", "Courier New", "DejaVu Sans Mono")
            item, ok = QInputDialog.getItem(self, "폰트 선택", "텍스트에 사용할 폰트를 골라주세요.", items)

            if ok:
                self.sld = Slide_ChangedText(item, self, items)


    # 색효과 기능 실행을 위한 함수
    def ColorEffect(self):
        self.sld = Slide_ColorEffect(self)
