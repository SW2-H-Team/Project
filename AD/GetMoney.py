from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button

class Store(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setUI()

    def setUI(self):
        mainlayout=QVBoxLayout()
        tablayout = QHBoxLayout()
        itemlayout = QGridLayout()

        self.setLayout(mainlayout)
        mainlayout.addWidget(QLabel('원하시는 상품을 구매하세요. '))
        mainlayout.addLayout(tablayout)
        mainlayout.addLayout(itemlayout)
        # 탭
        tab1=QWidget()
        tab2=QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, '도구')
        tabs.addTab(tab2, '색상')

        tablayout.addWidget(tabs)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    getmoney = GetMoney()
    getmoney.show()
    sys.exit(app.exec_())