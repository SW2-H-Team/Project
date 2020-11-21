from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Painter import Painter
from Store import Store
from GetMoney import GetMoney
from Button import Button

class MyApp(QWidget):

    def __init__(self,playername):
        super().__init__()

        self.playername=playername
        # 빚
        self.debt=20000000
        # 돈
        self.money=1000000000
        # 시간
        self.minute=0
        self.hour=0
        self.day=6
        self.week=0

        self.initUI()

    # 메인 UI
    def initUI(self):
        # 탭 레이아웃
        self.paintertab = Painter()
        self.storetab = Store(self)
        self.getmoneytab = GetMoney(self)

        tabs = QTabWidget()
        tabs.setFixedWidth(750)
        tabs.addTab(self.paintertab, '그림그리기')
        tabs.addTab(self.storetab, '상점')
        tabs.addTab(self.getmoneytab, '용돈벌기')

        tablayout = QVBoxLayout()
        tablayout.addWidget(tabs)

        #상태창
        statuslayout =  QHBoxLayout()

        self.namelabel = QLabel('이름: {}'.format(self.playername))
        self.moneylabel = QLabel('Money: {}'.format(self.money))
        self.timelabel = QLabel('시간 경과: {}m'.format(self.minute))

        statuslayout.addWidget(Button('save data', self.buttonClicked))
        statuslayout.addStretch()
        statuslayout.addWidget(self.namelabel)
        statuslayout.addStretch()
        statuslayout.addWidget(self.moneylabel)
        statuslayout.addStretch()
        statuslayout.addWidget(self.timelabel)

        # 가계부
        historylayout = QVBoxLayout()

        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFixedWidth(200)

        historylayout.addWidget(QLabel('가계부'))
        historylayout.addWidget(self.history)

        # 메인 레이아웃
        mainlayout = QGridLayout()
        mainlayout.addLayout(tablayout,0,0,5,5)
        mainlayout.addLayout(statuslayout,5,0,6,8)
        mainlayout.addLayout(historylayout,0,5,5,8)

        self.setLayout(mainlayout)
        self.setWindowTitle('AD')
        self.setGeometry(200, 120, 900, 600)
        self.show()

    # 모든 경제활동에서 발생하는 돈의 흐름
    def moneyUpdate(self,money,text):
        # 지출/수입 반영
        self.money += money
        self.moneylabel.setText('Money: {}'.format(self.money))

        # 가계부에 내용을 적습니다.
        historyold = self.history.toPlainText()
        self.history.setTextColor(QColor(255,0,0))# 현재의 기록은 강조하여 표시
        text = text.split('\n')
        text = text[0]+' ({}:{}:{}:{})\n'.format(self.week,self.day,self.hour,self.minute) +text[1]
        self.history.setText(text)
        self.history.append('= '+str(self.money))
        self.history.append('--------------------------------------')
        self.history.setTextColor(QColor(0,0,0))
        self.history.append(historyold)

    # 시간의 경과 표시
    def timeUpdate(self):
        self.minute += 1
        if self.minute ==60:
            self.getmoneytab.tab2.getNumber()
            self.hour +=1
            self.minute =0
        if self.hour ==24:
            self.day +=1
            self.hour =0
        if self.day ==7:
            self.week+=1
            self.day =0
            if self.debt:
                self.payBack()

        self.timelabel.setText('시간 경과: {}주 {}일 {}시간 {}분'.format(self.week,self.day,self.hour,self.minute))

    # 채무 상환
    def payBack(self):
        self.debt -= 1000000
        if self.money > 1000000:
            text = '채무 상환\n잔고: {} - {}'.format(self.money, 1000000)
            self.moneyUpdate(-1000000,text)
        else:
            # @@ 도구,색깔 있는지 판별
                # @@@ 있으면 뺏고 차감시켜
            text = '{} 압류당함.\n잔고: {} - {}'.format('$$',self.money,self.money)
            self.moneyUpdate(-self.money,text)
                # @@@ 없으면 게임오버


    ###################################################
    def buttonClicked(self):
        button = self.sender()

        self.money += 1000
        print(self.money)

        self.moneylabel.setText('Money: {}'.format(self.money))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp('김중현 ')
    sys.exit(app.exec_())

