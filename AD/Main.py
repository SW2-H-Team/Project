from PyQt5.QtWidgets import *

from Painter import Painter
from Store import Store
from GetMoney import GetMoney
from Button import Button

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.money=0
        self.time=0

        self.initUI()

    # 메인 UI
    def initUI(self):
        # 탭 레이아웃
        tab1 = Painter()
        tab2 = Store()
        tab3 = GetMoney(self)

        tabs = QTabWidget()
        tabs.addTab(tab1, '그림그리기')
        tabs.addTab(tab2, '상점')
        tabs.addTab(tab3, '용돈벌기')

        tablayout = QVBoxLayout()
        tablayout.addWidget(tabs)

        #상태창
        statuslayout =  QHBoxLayout()

        self.moneylabel = QLabel('Money: {}'.format(self.money))
        self.timelabel = QLabel('시간 경과: {}m'.format(self.time))

        statuslayout.addWidget(Button('save data', self.buttonClicked))
        statuslayout.addStretch(2)
        statuslayout.addWidget(self.moneylabel)
        statuslayout.addStretch(1)
        statuslayout.addWidget(self.timelabel)

        # 메인 레이아웃
        mainlayout = QVBoxLayout()
        mainlayout.addLayout(tablayout)
        mainlayout.addLayout(statuslayout)

        self.setLayout(mainlayout)
        self.setWindowTitle('AD')
        self.setGeometry(300, 150, 700, 500)
        self.show()

    # 모든 경제활동에서 발생하는 돈의 흐름
    def moneyUpdate(self,money):
        self.money += money
        self.moneylabel.setText('Money: {}'.format(self.money))

    # 시간의 경과 표시
    def timeUpdate(self):
        self.time += 1
        self.timelabel.setText('시간 경과: {}m'.format(self.time))

    def buttonClicked(self):
        button = self.sender()

        self.money += 100
        print(self.money)

        self.moneylabel.setText('Money: {}'.format(self.money))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())