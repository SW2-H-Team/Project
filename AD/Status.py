from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button

class Status(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.money=0
        self.time=[0,0,0,0]

        self.setUI()


    def setUI(self):
        mainlayout = QHBoxLayout()
        self.setLayout(mainlayout)

        self.currentmoney = QLabel('Money: {}'.format(self.money))
        self.currenttime = QLabel('Passing of Time: {}d {}h {}m'.format(0, 0, 0, 0))

        mainlayout.addWidget(Button('save data', self.buttonClicked))
        mainlayout.addStretch(2)
        mainlayout.addWidget(self.currentmoney)
        mainlayout.addStretch(1)
        mainlayout.addWidget(self.currenttime)


    def buttonClicked(self):
        button = self.sender()

        self.money += 100
        print(self.money)
        self.currentmoney.repaint()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    status = Status()
    status.show()
    sys.exit(app.exec_())
