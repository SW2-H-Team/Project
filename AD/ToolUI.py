from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Button import Button


class ToolUI(QWidget):
    def __init__(self,canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.tool()

    def tool(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.tools = [ Button('{}'.format(str(x)),self.buttonClicked) for x in range(7)]
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
        layout.addWidget(Button('1',self.buttonClicked))
        layout.addWidget(QLabel('배경색: '))
        layout.addWidget(Button('2',self.buttonClicked))

    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if fpath:
            self.image.save(fpath)

    def clear(self):
        self.canvas.image.fill(Qt.white)
        self.update()



    def buttonClicked(self):

        button = self.sender()
        key = button.text()
        print(key)
