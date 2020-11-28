import pickle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Painter import Painter
from Store import Store
from GetMoney import GetMoney
from Button import Button

# 로그인 화면
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

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
                # 현재 입력창의 텍스트를 이름으로 설정,
                name = self.nameinput.text()
                # 게임 실행
                self.close() #로그인 창은 끄고,
                ex = MyApp(name)

# 패배 화면
class DefeatWindow(QWidget):
    def __init__(self,status):
        super().__init__()

        self.name=status.playername
        self.time=status.time
        self.peakofmoney=status.peakofmoney

        self.setUI()

    def setUI(self):
        mainlayout=QVBoxLayout()
        recordlayout=QVBoxLayout()
        retrylayout=QVBoxLayout()

        namelabel=QLabel('이름: '+self.name)
        timelabel=QLabel('생존시간: {}주 {}일 {}시간 {}분'.format(self.time[0],self.time[1],self.time[2],self.time[3]))
        peakofmoneylabel=QLabel('최고 보유금액: '+str(self.peakofmoney))

        recordlayout.addWidget(namelabel)
        recordlayout.addWidget(timelabel)
        recordlayout.addWidget(peakofmoneylabel)

        defeatlabel = QLabel('파산했습니다. 다시하시겠습니까?')
        retrybutton=Button('다시하기',self.buttonClicked)
        retrybutton.setFixedSize(200,40)

        retrylayout.addStretch()
        retrylayout.addWidget(defeatlabel)
        retrylayout.addWidget(retrybutton)

        self.setLayout(mainlayout)
        mainlayout.addLayout(recordlayout)
        mainlayout.addLayout(retrylayout)
        self.setGeometry(200, 120, 900, 600)
        self.show()

    def buttonClicked(self):
        button=self.sender()
        if button.text()=='다시하기':
            self.close()
            self.ex = LoginWindow()

# 게임화면
class MyApp(QWidget):
    def __init__(self,name):
        super().__init__()
        # 데이터초기화
        self.totaldata={}
        self.data={'playername':name,'time':[0,0,0,0],'pom':1000000,'money':1000000,'debt':200000000,'history':'',
                   'bitcoins':[],'ore':[0,''],'brushcolors':{"Black": (0, 0, 0)}}

        self.dataLoad(name)
        # 사용자이름
        self.playername=self.data['playername']
        # 빚
        self.debt=self.data['debt']
        # 돈
        self.money=self.data['money']
        # 시간
        self.time = self.data['time']
        # 보유금액 최고기록
        self.peakofmoney=self.data['pom']

	    ## RGB값
        self.current_brush_color = self.data['brushcolors']
        self.a = 0
        self.b = 0
        self.c = 0

        self.initUI()

    # 시작시 데이터 불러오기
    def dataLoad(self,name):
        # 데이터파일 열기
        try:
            f = open('data.dat', 'rb')
            # 데이터에 불러온 데이터 저장
            try:
                totaldata = pickle.load(f)
                # 불러온 데이터에 현재 이름에 대한 정보가 있으면,
                if name in totaldata:
                    self.data = totaldata[name]  # 데이터를 덮어씌우기
                # 없으면,
                else:
                    totaldata[name] = self.data  # 사전에 새로운 이름에 대한 정보 추가,
                # 그리고 변수에 이 데이터를 저장
                self.totaldata = totaldata
            except:
                pass
            f.close()

        except FileNotFoundError:
            pass

    # 데이터 저장
    def dataSave(self):
        #
        self.data['time']=self.time
        self.data['pom']=self.peakofmoney
        self.data['money']=self.money
        self.data['debt']=self.debt
        self.data['history']=self.history.toPlainText()
        #비트코인의 이름, 보유량, x,y 를 저장
        for i in range(5):
            self.data['bitcoins'][i]['holding']=self.getmoneytab.tab1.bitcoins[i].holding
            self.data['bitcoins'][i]['x']=self.getmoneytab.tab1.bitcoins[i].x
            self.data['bitcoins'][i]['y']=self.getmoneytab.tab1.bitcoins[i].y
            self.data['bitcoins'][i]['investmentamount']=self.getmoneytab.tab1.bitcoins[i].investmentamount
        self.data['ore']=[self.getmoneytab.tab2.charge,self.getmoneytab.tab2.history]

        self.data['brushcolors']=self.current_brush_color

        self.totaldata[self.playername]=self.data
        #
        f = open('data.dat', 'wb')
        pickle.dump(self.totaldata, f)
        f.close()


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
        self.paintertab = Painter(self)
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
        self.timelabel = QLabel('시간 경과: {}m'.format(self.time[3]))

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
        self.history.setText(self.data['history'])
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

        # 최고보유금액갱신
        self.peakofmoneyUpdate()
        # 가계부에 내용을 적습니다.
        self.historyUpdate(text)

    # 가계부 갱신
    def historyUpdate(self,text):
        historyold = self.history.toPlainText()     #우선 현재의 가계부기록을 가져오고,
        self.history.setTextColor(QColor(255, 0, 0))  # 현재의 기록은 강조하여 표시
        text = text.split('\n')
        text = text[0] + ' ({}:{}:{}:{})\n'.format(self.time[0], self.time[1], self.time[2], self.time[3]) + text[1]
        self.history.setText(text)
        self.history.append('= ' + str(self.money)) #결과금액 표시
        self.history.append('--------------------------------------') #분리선
        self.history.setTextColor(QColor(0, 0, 0))
        self.history.append(historyold)

    # 최대 보유금액 갱신
    def peakofmoneyUpdate(self):
        if self.money > self.peakofmoney:
            self.peakofmoney=self.money

    # 시간의 경과 표시
    def timeUpdate(self):
        self.time[3] +=1 # 분
        if self.time[3] ==60: #60분 >1시간
            self.getmoneytab.tab2.getNumber() # 1시간마다 홀짝게임 결과 발표
            self.time[2]+=1
            self.time[3]=0
        if self.time[2] ==24: #24시간 > 1일
            self.time[1]+=1
            self.time[2]=0
        if self.time[1] ==7: # 7일 >1주
            self.time[0]+=1
            self.time[1]=0
            if self.debt: # 일주일마다 채무 상환
                self.payBack()
                self.checkDefeated() #파산크

        self.timelabel.setText('시간 경과: {}주 {}일 {}시간 {}분'.format(self.time[0],self.time[1],self.time[2],self.time[3]))

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

    # 패배 체크
    def checkDefeated(self):
        if self.bankrupt():
            for i in self.getmoneytab.tab1.bitcoins: # 시간이 흐르지않게 막아줌
                i.ani._stop()
            self.close() #현재화면을 끄고,
            self.ex = DefeatWindow(self) #패배화면을 띄운다.

    # 파산감지
    def bankrupt(self):
        # 현금, 비트코인 보유량, 홀짝게임충전금이 전부 없으면,(파산하면)
        if self.money==0 :
            if self.getmoneytab.tab2.charge==0:
                for i in self.getmoneytab.tab1.bitcoins:
                    if i.holding !=0:
                        return False
                return True

    # 승리체크
    def victory(self):
        pass

    ###################################################
    def buttonClicked(self):
        button = self.sender()

        if button.text()=='save data':
            reply = QMessageBox.question(self, '저장하기', '지금까지의 데이터를 저장하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.dataSave()
                print('저장됨')
############################################
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    ex = LoginWindow()
    sys.exit(app.exec_())
