from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Button import Button

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class Bitcoin(QWidget):
    def __init__(self,name,status,holding=0,x=[0],y=[np.random.randint(6000, 12000)],investmentamount=0):
        super().__init__()

        self.setFixedSize(680,200)
        self.status=status

        self.x = x
        self.y = y
        # 그래프 기울기
        self.economy = 0
        self.adjustment= 1
        self.gradient= 0.001
        self.subgradient = 0

        # 그래프 시각화
        self.fig = Figure(figsize=(4.5, 2))
        self.ax = self.fig.add_subplot(ylim=(0, self.y[0] * 3), xlim=(0,60))
        self.canvas = FigureCanvas(self.fig)
        self.line, = self.ax.plot(self.x, self.y,color='red', animated=True, lw=1)
        self.ani = animation.FuncAnimation(self.fig, self.updateLine, blit=True, interval=50)
        # 그래프 속성
        self.itemname = name        #종목이름
        self.price = self.y[-1] #매입가
        self.holding=holding         #보유량

        self.investmentamount = investmentamount # 총 투자금액
        self.presentvalue = self.price*self.holding # 현재 보유중인 코인의 가치

        self.setUI()


    def setUI(self):
        #레이아웃
        mainlayout = QHBoxLayout()
        rightlayout = QGridLayout()
        leftlayout = QVBoxLayout()

        mainlayout.addLayout(leftlayout)
        mainlayout.addLayout(rightlayout)
        self.setLayout(mainlayout)

        # 그래프
        leftlayout.addWidget(self.canvas)
        # 비트코인 속성
        self.itemnamelabel = QLabel(self.itemname)
        itemnamefont=QFont('KacstOne',10)
        itemnamefont.setBold(True)
        self.itemnamelabel.setFont(itemnamefont)
        self.pricelabel = QLabel('매입가: {:,}원'.format(self.price))
        self.holdinglabel = QLabel('보유량: {:,}개'.format(self.holding))
        self.presentvaluelabel = QLabel('코인 현재가치: {:,}원'.format(self.presentvalue))
        self.gnllabel = QLabel('평가손익: {:,}원'.format(self.presentvalue - self.investmentamount))

        # 매수,매도버튼
        rightlayout.addWidget(self.itemnamelabel, 0, 0)
        rightlayout.addWidget(self.pricelabel,2,0,3,2)
        rightlayout.addWidget(self.holdinglabel,3,0,4,2)
        rightlayout.addWidget(self.presentvaluelabel,4,0,5,2)
        rightlayout.addWidget(self.gnllabel, 5, 0,6,2)

        buyingbutton = Button('매수', self.buttonClicked)
        sellingbutton = Button('매도', self.buttonClicked)
        buyingbutton.setFixedSize(120,30)
        sellingbutton.setFixedSize(120,30)
        rightlayout.addWidget(buyingbutton,7,0,8,1)
        rightlayout.addWidget(sellingbutton,7,1,8,2)

    def buttonClicked(self):
        button = self.sender()
        if button.text() =='매수':
            buying, ok = QInputDialog.getInt(self, '매수 수량', '매수 수량을 입력하세요.\n최대 매수가능량: {}개'
                                             .format(self.status.money//self.price))
            investment = self.price * buying

            if ok:
                if buying <= 0:  # 예외처리
                    QMessageBox.warning(self, '경고!', '0 보다 큰 수를 입력해주세요.', QMessageBox.Ok)
                elif investment > self.status.money:
                    QMessageBox.warning(self, '경고!', '보유 금액이 부족합니다.', QMessageBox.Ok)
                else:
                    self.holding+=buying
                    self.investmentamount+=investment
                    # 보유금액에서 차감
                    text= '{} {:,}개 매수\n잔고: {:,} - {:,}'.format(self.itemname,buying,self.status.money,investment)
                    self.status.moneyUpdate(-1*self.price*buying,text)


        elif button.text() =='매도':
            selling, ok = QInputDialog.getInt(self, '매도 수량', '매도 수량을 입력하세요. 수수료 8%\n현재 코인 보유량: {}'
                                              .format(self.holding))

            if ok:
                if not 0<selling <=self.holding: #예외처리
                    QMessageBox.warning(self, '경고!', '{:,}이하의 자연수를 입해주세요.'.format(self.holding), QMessageBox.Ok)
                else:
                    self.holding -= selling
                    self.investmentamount -= self.price * selling
                    # 보유금액에 증가
                    text = '{} {:,}개 매도\n잔고: {:,} + {:,}'.format(self.itemname, selling, self.status.money, self.price*selling)
                    self.status.moneyUpdate(int(self.price*selling*0.92),text)
                    self.status.showAchievement()
            if not self.holding:
                self.investmentamount=0

        self.holdinglabel.setText('보유량: {:,}개'.format(self.holding))
    # 그래프 기울기 관리
    def changeEconomy(self):
        random = np.random.randint(1,1001)
        if random <= 20: return True  # 2%
        else: return False

    def changeGradient(self):
        random= np.random.randint(1,21)
        if random<=6: return True #30%
        else: return False

    # 코인의 경제상황 (개별적인 그래프 변화율)
    def updateEconomy(self):
        random = np.random.randint(1, 101)
        if random <= 4:       #4%
            self.economy = -7
        elif random < 20:     #16%
            self.economy = -3.3
        elif random <= 40:     # 22%        #경기불황 42%
            self.economy = -1.5
        elif random <= 64:     #20% 보통
            self.economy = 0  # 기댓값 0.082
        elif random <= 82:  # 20%            #경기 호황 38%
            self.economy = 1.8
        elif random <= 96:    #14%
            self.economy = 4
        else:  #4%
            self.economy = 7.5

    # 코인의 기울기설정
    def updateGradient(self):
        #기울기 = 조정함수*정규분포*경제상황
        self.gradient= self.adjustment*(np.random.normal(0,0.004,1)[0]+0.001* self.economy)

    # 그래프 과도한 성장 제한
    def setAdjustment(self):
        if self.price<600 and self.gradient>0:
            self.adjustment=1.5
        elif self.price<4000 and self.gradient>0:
            self.adjustment=1.2
        elif self.price<10000:
            self.adjustment=1
        elif self.price<40000:
            self.adjustment=0.9
        elif self.price<70000:
            self.adjustment=0.8
        elif self.price<100000:
            self.adjustment=0.7
        elif self.price<500000:
            self.adjustment=0.5
        elif self.price<1000000:
            self.adjustment=0.3
        else:
            self.adjustment=0.1

    # 그래프의 역동적인 모습을 만들기 위한 그래프
    def setSubgradient(self):
        if self.price <1000:
            self.subgradient = 0.0001* np.random.randint(300,500,1)[0]
        elif self.price <10000:
            self.subgradient = 0.0001* np.random.normal(0,1000,1)[0]
        else:
            self.subgradient = 0.0001* np.random.normal(0,900,1)[0]

    # y축 재설정
    def setYLim(self):
        if self.price <10000:
            self.ax.set_ylim(0, self.y[0]*3)
        elif self.price <100000:
            self.ax.set_ylim(self.y[0]*0.2,self.y[0]*2.5)
        elif self.price < 1000000:
            self.ax.set_ylim(self.y[0]*0.3,self.y[0]*2.2)
        else:
            self.ax.set_ylim(self.y[0]*0.4,self.y[0]*2)

    # 그래프 갱신
    def updateLine(self, i):
        # 60초가 채워지면 그래프 다시그리기
        lastx=self.x[-1]
        if lastx > self.x[0]+59:
            self.x = [0]
            self.y = [self.y[-1]]
            self.ax.set_xlim(self.x[0],self.x[0]+60)
            self.setYLim()
            self.ax.figure.canvas.draw()
        # 값 갱신

        if self.changeEconomy():
            self.updateEconomy()
        if self.changeGradient():
            self.updateGradient()
        self.setAdjustment()
        self.setSubgradient()

        x = self.x[-1] + 1
        y = int((1+self.gradient+self.subgradient)*self.y[-1])

        self.x.append(x)
        self.y.append(y)

        self.line.set_data(self.x,self.y)

        # 내용 갱신
        self.price = self.y[-1]
        self.presentvalue = self.price * self.holding

        self.pricelabel.setText('매입가: {:,}원'.format(self.price))
        self.presentvaluelabel.setText('현재가치: {:,}원'.format(self.presentvalue))
        self.gnllabel.setText('평가손익: {:,}원'.format(int(0.92*self.presentvalue) - self.investmentamount))

        # 시간갱신
        if self.itemname == self.status.data['bitcoins'][0]['itemname']:
            self.status.timeUpdate()

        return [self.line]

class BitcoinMarket(QWidget):
    def __init__(self,status):
        super().__init__()

        self.status=status

        self.setUI()

    def setUI(self):
        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        # 비트코인 목록창
        scrollarea = QScrollArea()
        scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        bitcoins = QGroupBox()
        vbox = QVBoxLayout()
        bitcoins.setLayout(vbox) # 그룹박스에는 레이아웃을 넣어야함

        ## 비트코인 생성
        self.bitcoins=[]
        # 불러온 데이터의 정보를 그대로 사용
        if self.status.data['bitcoins']:
            for i in range(5):
                self.bitcoinLoad(self.status,i,vbox)
        # 새로운 데이터의 경우 비트코인을 새로 생성
        else:
            for i in range(5):
                self.bitcoinGenerate(vbox)

        scrollarea.setWidget(bitcoins)

        mainlayout.addWidget(scrollarea)

    # 비트코인 이름만들기
    def setBitcoinName(self):
        name = ''
        for i in range(5):
            random=np.random.randint(0,2)
            if random==0: #대문자
                name += chr(np.random.randint(65,91))
            else:
                name += chr(np.random.randint(97,123))
        return name

    # 비트코인 불러오기
    def bitcoinLoad(self,status,index,layout):
        name = self.status.data['bitcoins'][index]['itemname']
        holding = self.status.data['bitcoins'][index]['holding']
        x= self.status.data['bitcoins'][index]['x']
        y= self.status.data['bitcoins'][index]['y']
        investmentamount=self.status.data['bitcoins'][index]['investmentamount']
        oldbitcoin = Bitcoin(name,status,holding,x,y,investmentamount)
        layout.addWidget(oldbitcoin)
        self.bitcoins.append(oldbitcoin)

    # 비트코인 생성
    def bitcoinGenerate(self,layout):
        name = self.setBitcoinName() #비트코인 이름을 만들고,
        newbitcoin = Bitcoin(name,self.status) #그 이름을 갖고 비트코인을 생성한다음,
        layout.addWidget(newbitcoin) # 생선한 비트코인을 비트코인 마켓에 추가한다.
        self.status.data['bitcoins'].append({
            'itemname':name,'holding':0,'x':[0],'y':newbitcoin.y,'investmentamount':0}) # 메인의 데이터에 이 비트코인 정보를 저장한다.
        self.bitcoins.append(newbitcoin)  # 마지막으로 메인의 데이터에 이 비트코인 정보를 추가한다.


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    bcmarket = BitcoinMarket()
    bcmarket.show()
    sys.exit(app.exec_())