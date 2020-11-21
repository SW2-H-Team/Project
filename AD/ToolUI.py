from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Button import Button
import Canvas


class ToolUI(QWidget):
    def __init__(self,canvas,painter, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.painter = painter
        self.tool()



    def tool(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.tools = [ Button('{}'.format(str(x)),self.buttonClicked) for x in range(5)]

        self.tools.append(Button('빨강펜',self.buttonClicked))
        self.tools.append(Button('파랑펜',self.buttonClicked))

        self.tools.append(Button('저장',self.save))
        self.tools.append(Button('지우기',self.clear))

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)



        for i in range(len(self.tools)):
            layout.addWidget(self.tools[i])
        layout.addStretch()

        #색상
        layout.addWidget(QLabel('전경색: '))
        #layout.addWidget(Button('1', self.foregroundColor()))
        layout.addWidget(QLabel('배경색: '))
        #layout.addWidget(Button('2',self.backgroungColor()))

    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png) ")

        if fpath:
            self.canvas.image.save(fpath + '.png')
            # 혹시 다른 확장자로 바꾸거나 .png.png 로 저장되는 걸 수정하고 싶으면 이 부분 고치


    def clear(self):
        self.canvas.image.fill(Qt.white)
        self.update()


    #def foregroundColor(self):
    #    Canvas.ChangedColor(Qt.red)

    #def backgroungColor(self):
    #    Canvas.ChangedColor(Qt.white)

    def ChangedColor(self, color):
        self.canvas.brush_color = color

    def ChangedSize(self, size):
        self.canvas.brush_size = size



    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key=='빨강펜':
            self.ChangedColor(Qt.red)

        elif key=='파랑펜':
            self.ChangedColor(Qt.blue)
