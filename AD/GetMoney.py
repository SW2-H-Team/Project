from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button
from Bitcoin import *

class GetMoney(QWidget):

    def __init__(self,status):
        super().__init__()

        self.status=status

        self.setUI()

    def setUI(self):
        mainlayout=QVBoxLayout()
        tablayout = QHBoxLayout()

        self.setLayout(mainlayout)
        mainlayout.addLayout(tablayout)
        # 탭
        tab1=BitcoinMarket(self.status)
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