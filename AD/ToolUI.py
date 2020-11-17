from PyQt5.QtWidgets import *

from Button import Button


class ToolUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tool()

    def tool(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        tools = [ Button('{}'.format(str(x)),self.buttonClicked) for x in range(9)]
        for i in range(len(tools)):
            layout.addWidget(tools[i])
        layout.addStretch()

        #색상
        layout.addWidget(QLabel('전경색: '))
        layout.addWidget(Button('1',self.buttonClicked))
        layout.addWidget(QLabel('배경색: '))
        layout.addWidget(Button('2',self.buttonClicked))

    def buttonClicked(self):

        button = self.sender()
        key = button.text()
        print(key)
