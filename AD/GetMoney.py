from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button

class GetMoney(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setUI()

    def setUI(self):
        mainlayout=QVBoxLayout()
        tablayout = QHBoxLayout()

        self.setLayout(mainlayout)
        mainlayout.addLayout(tablayout)
        # 탭
        tab1=QWidget()
        tab2=QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, '비트코인')
        tabs.addTab(tab2, '홀짝')

        tablayout.addWidget(tabs)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    getmoney = GetMoney()
    getmoney.show()
    sys.exit(app.exec_())