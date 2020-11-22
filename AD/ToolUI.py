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

        #self.tools = [Button('{}'.format(str(x)), self.buttonClicked) for x in range(2)]
        self.tools = []

        self.tools.append(Button('그리기', self.buttonClicked))
        self.tools.append(Button('직선', self.buttonClicked))
        self.tools.append(Button('선모드', self.buttonClicked))
        self.tools.append(Button('색효과', self.buttonClicked))
        self.tools.append(Button('스포이드', self.buttonClicked))
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
            self.canvas.brush_size = self.save_brush_size
            self.save_brush_size = self.change('선 굵기', '50', self.save_brush_size)
            self.ChangedValue(self.save_brush_color, self.save_brush_size)

        elif key == '지우개':
            self.canvas.save_drawingType = 'drawing'
            self.save_eraser_size = self.change('지우개 굵기', '50', self.save_eraser_size)
            self.ChangedValue(QColor(255, 255, 255), self.save_eraser_size)

        elif key == '직선':
            self.canvas.save_drawingType = 'line'
            self.canvas.brush_size = self.save_line_size
            self.save_line_size = self.change('직선 굵기', '50', self.save_line_size)
            self.ChangedValue(self.save_brush_color, self.save_line_size)

        elif key == '선모드':
            self.canvas.brush_mode = self.save_brush_mode
            self.save_brush_mode = self.changingMode('선의 모드', '4', self.save_brush_mode)
            self.canvas.brush_mode = self.save_brush_mode

        elif key == '색효과':
            pass

        elif key == '스포이드':
            pass




    # 굵기 정하는 창 띄워주는 함수
    def Thickness(self, thicknessType, maxThickness, saveValue):  # (원하는 굵기 종류, 굵기의 최대 범위, cancel 시 반환할 값)
        while True:
            thickness, ok = QInputDialog.getText(self, '{}'.format(thicknessType),
                                                 '원하는 굵기를 선택하세요.\n최대 굵기: {}'.format(maxThickness))
            if ok == False:
                return saveValue
            if thickness == '':
                QMessageBox.warning(self, '경고!', '숫자를 입력하세요.', QMessageBox.Ok)
                continue
            elif thickness.isdigit():
                pass
            else:
                QMessageBox.warning(self, '경고!', '값이 이상합니다. 다시 입력해주세요.', QMessageBox.Ok)
                continue

            thickness = int(thickness)

            if thickness <= 0:  # 예외처리
                QMessageBox.warning(self, '경고!', '0 보다 큰 수를 입력하세요.', QMessageBox.Ok)
                continue
            elif thickness > int(maxThickness):
                QMessageBox.warning(self, '경고!', '{} 보다 작은 수를 입력하세요.'.format(maxThickness), QMessageBox.Ok)
                continue
            else:
                if ok:
                    return thickness



    # 변경할 것인지 물어보는 창 띄워주는 함수
    def change(self, changingType, limit, saveValue):
        result = saveValue
        answer = QMessageBox.question(self, '질문', '{}를 변경할까요?'.format(changingType),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.save_point = self.Thickness('{}'.format(changingType),
                                                       '{}'.format(limit), saveValue)
            result = self.save_point
        else:
            pass

        return result


    # 선모드 선택 
    def changingMode(self, changingType, limit, saveValue):
        text = '원하는 모드를 선택하세요.\n0 : 실선\n1 : 짧은실선\n2 : 점선\n3 : 실점선'
        list = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, ]
        result = saveValue
        answer = QMessageBox.question(self, '질문', '{}를 변경할까요?'.format(changingType),
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            while True:
                thickness, ok = QInputDialog.getInt(self, '{}'.format(changingType), text)
                if ok == False:
                    break
                elif thickness > 3:
                    QMessageBox.warning(self, '경고!', '{} 보다 작은 수를 입력하세요.'.format(limit), QMessageBox.Ok)
                    continue
                else:
                    result = list[thickness]
                    break
        else:
            pass

        return result





    # 현재 무슨 색인지 텍스트로 알려주기
    def nowColor(self):
        pass
