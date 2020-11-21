from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button
from Bitcoin import *
from OddOrEven import *

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
        self.tab1=BitcoinMarket(self.status)
        self.tab2=OddOrEven(self.status)

        tabs = QTabWidget()
        tabs.addTab(self.tab1, '비트코인')
        tabs.addTab(self.tab2, '홀짝')

        tablayout.addWidget(tabs)

if __name__ == '__main__':
    from Main import *
    import sys

    app = QApplication(sys.argv)
    getmoney = GetMoney(MyApp('dd'))
    getmoney.show()
    sys.exit(app.exec_())