import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Painter import Painter
from Store import Store
from GetMoney import GetMoney
from Button import Button

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.name=''

        self.setUI()

    def setUI(self):
        mainlayout = QGridLayout()
        self.setLayout(mainlayout)

        gametitle = QLabel('윤고딕 72pt')
        self.nameinput = QLineEdit()
        self.nameinput.setFixedSize(200,30)
        inputbutton = Button('로그인',self.buttonClicked)
        inputbutton.setFixedSize(100,50)

        mainlayout.addWidget(gametitle,2,2,2,8)
        mainlayout.addWidget(self.nameinput,4,3,4,7)
        mainlayout.addWidget(inputbutton,5,4,5,6)

        self.setGeometry(200, 120, 900, 600)
        self.show()

    def buttonClicked(self):
        button = self.sender()
        if button.text()=='로그인':
            # 이름 설정
            # 아무것도 입력되지 않으면,
            if len(self.nameinput.text())==0:
                QMessageBox.warning(self, '경고!', '뭐라도 입력하세요.', QMessageBox.Ok)
            # 입력되면,
            else:
                self.name = self.nameinput.text()
                # 데이터 불러오기


                # 게임 실행
                self.close() #로그인 창은 끄고,
                ex = MyApp(self)

class MyApp(QWidget):

    def __init__(self,main):
        super().__init__()

        self.playername=main.name
        # 빚
        self.debt=200000000
        # 돈
        self.money=1000000
        # 시간
        self.minute=0
        self.hour=23
        self.day=6
        self.week=0
        ## painter 관련
        # 보유한 색깔
        self.colors=[]
        ## bitcoin관련
        # 그래프 현황
        self.graphx=[]
        self.graphy=[]
        ## 홀짝게임 현황
        self.charge =[]
        self.history=[]
        ##




        self.initUI()

    # 메인 UI
    def initUI(self):
        # 메인 레이아웃
        mainlayout = QGridLayout()
        statuslayout = QHBoxLayout()
        tablayout = QVBoxLayout()
        historylayout = QVBoxLayout()

        mainlayout.addLayout(tablayout, 0, 0, 5, 5)
        mainlayout.addLayout(statuslayout, 5, 0, 6, 8)
        mainlayout.addLayout(historylayout, 0, 5, 5, 8)

        # 탭 레이아웃
        self.paintertab = Painter()
        self.storetab = Store(self)
        self.getmoneytab = GetMoney(self)

        tabs = QTabWidget()
        tabs.setFixedWidth(750)
        tabs.addTab(self.paintertab, '그림그리기')
        tabs.addTab(self.storetab, '상점')
        tabs.addTab(self.getmoneytab, '용돈벌기')

        tablayout.addWidget(tabs)

        #상태창


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


        self.historylabel = QLabel('가계부\t\t남은 빚: {}'.format(self.debt))
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFixedWidth(200)

        historylayout.addWidget(self.historylabel)
        historylayout.addWidget(self.history)



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
            self.getmoneytab.tab2.getNumber() # 1시간마다 홀짝게임 결과 발표
            self.hour +=1
            self.minute =0
        if self.hour ==24:
            self.day +=1
            self.hour =0
        if self.day ==7:
            self.week+=1
            self.day =0
            if self.debt: # 일주일마다 채무 상환
                self.payBack()

        self.timelabel.setText('시간 경과: {}주 {}일 {}시간 {}분'.format(self.week,self.day,self.hour,self.minute))

    # 채무 상환
    def payBack(self):
        self.debt -= 1000000
        self.historylabel.setText('가계부\t\t남은 빚: {}'.format(self.debt))
        if self.money >= 1000000:
            text = '채무 상환\n잔고: {} - {}'.format(self.money, 1000000)
            self.moneyUpdate(-1000000,text)
        else:
            # @@ 도구,색깔 있는지 판별
                # @@@ 있으면 뺏고 차감시켜
            text = '{} 압류당함.\n잔고: {} - {}'.format('$$',self.money,self.money)
            self.moneyUpdate(-self.money,text)
                # @@@ 없으면 게임오버

    # 파산, 패배처
    def bankruptcy(self):
        if not self.colors and self.money==0:
            return True


    ###################################################
    def buttonClicked(self):
        button = self.sender()

        self.money += 1000
        print(self.money)

        self.moneylabel.setText('Money: {}'.format(self.money))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = LoginWindow()
    sys.exit(app.exec_())