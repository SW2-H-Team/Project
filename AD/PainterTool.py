from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Button import Button
from Slide import *

class PainterTool(QWidget):
    """
    그림판에서 그리기 설정을 할 수 있는 도구가 있는 클래스입니다.
    다양한 기능과 색깔을 이용해 그림을 그리고 그린 그림은 저장할 수 있습니다.
    """
    def __init__(self, canvas, status, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.status = status

        # canvas와 연계되는 도구 값 저장 변수
        self.save_eraser_size = 5
        self.save_brush_size = 5
        self.save_line_size = 5
        self.save_brush_mode = Qt.SolidLine
        self.save_point = 5

        self.save_red = 0
        self.save_blue = 0
        self.save_green = 0
        self.save_alpha = 255
        self.save_brush_color = QColor(self.save_red, self.save_green, self.save_blue, self.save_alpha)


        self.setUI()

    # tool의 UI
    def setUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        # self.tools = [Button('{}'.format(str(x)), self.buttonClicked) for x in range(2)]
        self.tools = []

        self.tools.append(Button('그리기', self.buttonClicked))
        self.tools.append(Button('직선', self.buttonClicked))
        self.tools.append(Button('지우개', self.buttonClicked))
        self.tools.append(Button('선굵기', self.buttonClicked))
        self.tools.append(Button('선모드', self.buttonClicked))
        self.tools.append(Button('투명도', self.buttonClicked))
        self.tools.append(Button('텍스트', self.buttonClicked))

        self.tools.append(Button('저장', self.save))
        self.tools.append(Button('지우기', self.clear))

        self.tools[0].setCheckable(True)
        self.tools[0].toggle() #기본으로 브러쉬를 사용
        self.tools[1].setCheckable(True)
        self.tools[2].setCheckable(True)


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
        for i in range(0, 4):
            layout.addWidget(QLabel())
        layout.addWidget(QLabel('색 바꾸기: '))

        # 색상 선택
        self.cb = QComboBox(self)
        for i in list(self.status.data['brushcolors'].keys()): #저장됐던 색상들 불러오기.
            self.cb.addItem(i)
        layout.addWidget(self.cb)

        self.cb.currentIndexChanged.connect(self.comboBoxFunction)

        # 선택한 색 보이기
        self.label = QLabel()
        self.label.setStyleSheet('color:free; background:rgb({},{},{},{})'.
                                 format(self.save_red, self.save_green, self.save_blue, self.save_alpha))
        layout.addWidget(self.label, 1)

    # canvas로 전달
    def comboBoxFunction(self):
        self.save_red = self.status.current_brush_color[self.cb.currentText()][0]
        self.save_green = self.status.current_brush_color[self.cb.currentText()][1]
        self.save_blue = self.status.current_brush_color[self.cb.currentText()][2]
        self.save_brush_color = QColor(self.save_red, self.save_green, self.save_blue, self.save_alpha)
        self.label.setStyleSheet('color:free; background:rgb({},{},{},{})'.
                                 format(self.save_red, self.save_green, self.save_blue, self.save_alpha))
        self.ChangedColor(self.save_brush_color)

    # ------------------------------------------------------------------------ #


    # 그린 그림 저장하기
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

    # 색깔 변경시 라벨에 해당 색을 보여주고 색을 변경한다.
    def ChangedColor(self, color):
        self.label.setStyleSheet('color:free; background:rgb({},{},{},{})'.
                                 format(self.save_red, self.save_green, self.save_blue, self.save_alpha))
        self.canvas.brush_color = color

    # 브러쉬 크기 변경
    def ChangedSize(self, size):
        self.canvas.brush_size = size

    # 브러쉬 RGB값 변경
    def ChangedRGBA(self, r, g, b, a):
        self.save_red = r
        self.save_green = g
        self.save_blue = b
        self.save_alpha = a
        self.label.setStyleSheet('color:free; background:rgb({},{},{},{})'.
                                 format(self.save_red, self.save_green, self.save_blue, self.save_alpha))
        self.ChangedColor(self.MakeColor())

    # RGB값을 배합해서 색상 리턴
    def MakeColor(self):
        self.save_brush_color = QColor(self.save_red, self.save_green, self.save_blue, self.save_alpha)
        return self.save_brush_color

    # 그리기 설정 총 변화
    def ChangedValue(self, color, size, mode):
        self.ChangedColor(color)
        self.ChangedSize(size)
        self.canvas.brush_mode = mode

    # 텍스트의 글씨체 바꾸기
    def ChangedFont(self, font, size):
        self.canvas.stringFont = font
        self.canvas.stringFontSize = size


    # ----------------------------------------------------------------------- #


    # 도구의 각 버튼 입력시
    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '그리기':
            # 한번에 한 버튼만 눌리게.
            if not self.tools[0].isChecked():
                self.tools[0].toggle()
            elif self.tools[1].isChecked():
                self.tools[1].toggle()
            elif self.tools[2].isChecked():
                self.tools[2].toggle()
            self.canvas.save_drawingType = 'drawing'
            self.ChangedValue(self.save_brush_color, self.save_brush_size, self.save_brush_mode)

        elif key == '지우개':
            if self.tools[0].isChecked():
                self.tools[0].toggle()
            elif self.tools[1].isChecked():
                self.tools[1].toggle()
            elif not self.tools[2].isChecked():
                self.tools[2].toggle()
            self.canvas.save_drawingType = 'drawing'
            self.ChangedValue(QColor(255, 255, 255, 255), self.save_eraser_size, Qt.SolidLine)

        elif key == '직선':
            if self.tools[0].isChecked():
                self.tools[0].toggle()
            elif not self.tools[1].isChecked():
                self.tools[1].toggle()
            elif self.tools[2].isChecked():
                self.tools[2].toggle()
            self.canvas.save_drawingType = 'line'
            self.ChangedValue(self.save_brush_color, self.save_line_size, self.save_brush_mode)

        elif key == '선모드':
            self.save_brush_mode = self.changingMode()
            self.canvas.brush_mode = self.save_brush_mode
            self.ChangedValue(self.save_brush_color, self.save_brush_size, self.save_brush_mode)

        elif key == '선굵기':
            self.setThickness()

        elif key == '투명도':
            self.ColorEffect()

        elif key == '텍스트':
            self.canvas.save_drawingType = 'text'
            self.ChangedText()

    # 굵기 정하는 창 띄워주는 함수
    def setThickness(self):
        self.sld = Slide_Thickness(self)

    # 선모드를 변경할 것인지 물어보는 창 띄워주는 함수
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

    # 색효과(투명도 조절) 기능 실행을 위한 함수
    def ColorEffect(self):
        self.sld = Slide_ColorEffect(self)
