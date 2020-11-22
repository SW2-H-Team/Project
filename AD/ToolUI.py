from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Button import Button


class ToolUI(QWidget):
    def __init__(self, canvas, painter, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.painter = painter
        self.save_eraser_size = 5
        self.save_brush_size = 5
        self.save_line_size = 5
        self.save_brush_mode = Qt.SolidLine
        self.save_brush_color = QColor(0, 0, 0)
        self.save_point = 5
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

        # 색상         >> 메시지 남김 : 원래 전경색이었는데 색 바꾸기로 그냥 이름 바꿨어!
        layout.addWidget(QLabel('색 바꾸기: '))
        # layout.addWidget(Button('1', self.foregroundColor()))
        # layout.addWidget(QLabel('배경색: '))
        # layout.addWidget(Button('배경', self.buttonClicked()))
        # layout.addWidget(QLabel('현재 색깔: '))

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

    def spoid(self, e):
        pass

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
            pass

        elif key == '텍스트':
            self.canvas.save_drawingType = 'text'


    # 굵기 정하는 창 띄워주는 함수
    def Thickness(self):  # (원하는 굵기 종류, 굵기의 최대 범위, cancel 시 반환할 값)

        # 어떤 굵기를 바꿀 것인지
        items = ("그리기", "직선", "지우개")
        item, ok = QInputDialog.getItem(self, "선굵기", "변경하고 싶은 굵기를 골라주세요.", items, 0, False)

        if ok == False:
            pass
        else:
            # 이 부분에 슬롯 넣기
            if item == item[0]:
                self.save_brush_size = self.save_size
            elif item == item[1]:
                self.save_line_size = self.save_size
            else:
                self.save_eraser_size = self.save_size


    # 변경할 것인지 물어보는 창 띄워주는 함수
    def changingMode(self):
        # 어떤 모드를 선택할 것인 것인지
        items = ("실선", "짧은실선", "점선", "실점선")
        list = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, ]
        result = self.save_brush_mode

        item, ok = QInputDialog.getItem(self, "선모드", "바꾸고자 하는 모드를 골라주세요.", items, 0, False)

        if ok == False:
            pass
        else:
            if item == items[0]:
                result = list[0]
            elif item == items[1]:
                result = list[1]
            elif item == items[2]:
                result = list[2]
            else:
                result = list[3]

        return result


    # 현재 무슨 색인지 텍스트로 알려주기
    def nowColor(self):
        pass
