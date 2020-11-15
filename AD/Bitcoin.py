from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Button import Button

import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class Bitcoin(QWidget):
    def __init__(self,name,status):
        super().__init__()
        self.status=status

        self.x = [0]
        self.y = [random.randint(500, 3000)]
        # 그래프 기울기
        self.economy = 0
        self.adjustment= 1
        self.gradient= 0.001
        self.subgradient = 0


        self.fig = Figure(figsize=(5, 2))
        self.ax = self.fig.add_subplot(ylim=(self.y[0] * 0.5, self.y[0] * 1.5 ), xlim=(0,60))
        self.canvas = FigureCanvas(self.fig)

        self.line, = self.ax.plot(self.x, self.y,color='red', animated=True, lw=1)

        self.itemname = name        #종목이름
        self.price = self.y[-1] #매입가
        self.holding=0          #보유량

        self.investmentamount = 0 # 총 투자금액
        self.presentvalue = self.price*self.holding # 현재 보유중인 코인의 가치

        self.setUI()
        self.ani = animation.FuncAnimation(self.fig, self.updateLine, blit=True, interval=10)

    def setUI(self):
        mainlayout = QHBoxLayout()
        rightlayout = QGridLayout()
        leftlayout = QVBoxLayout()

        mainlayout.addLayout(leftlayout)
        mainlayout.addLayout(rightlayout)
        self.setLayout(mainlayout)

        leftlayout.addWidget(self.canvas)

        self.pricelabel = QLabel('매입가: {}'.format(self.price))
        self.holdinglabel = QLabel('보유량: {}'.format(self.holding))
        self.presentvaluelabel = QLabel('코인 현재가치: {}'.format(self.presentvalue))
        self.gnllabel = QLabel('평가손익: {}'.format(self.presentvalue - self.investmentamount))

        rightlayout.addWidget(QLabel(self.itemname), 0, 0)
        rightlayout.addWidget(self.pricelabel,1,0)
        rightlayout.addWidget(self.holdinglabel,3,0)
        rightlayout.addWidget(self.presentvaluelabel,4,0)
        rightlayout.addWidget(self.gnllabel, 5, 0)

        buyingbutton = Button('매수', self.buttonClicked)
        sellingbutton = Button('매도', self.buttonClicked)
        rightlayout.addWidget(buyingbutton,7,0)
        rightlayout.addWidget(sellingbutton,7,1)

    def buttonClicked(self):
        button = self.sender()
        print(button.text())
        if button.text() =='매수':
            buying, ok = QInputDialog.getInt(self, '매수 수량', '매수 수량을 입력하세요.')
            investment = self.price * buying
            if buying<0 : #예외처리
                QMessageBox.warning(self, '경고!', '0 이상의 수를 입력해주세요.',QMessageBox.Ok)
            elif investment >self.status.money:
                QMessageBox.warning(self, '경고!', '보유 금액이 부족합니다.', QMessageBox.Ok)
            else:
                if ok:
                    self.holding+=buying
                    self.investmentamount+=investment
                    # 보유금액에서 차감
                    text= '{} {}개 매수\n잔고: {} - {}'.format(self.itemname,buying,self.status.money,investment)
                    self.status.moneyUpdate(-1*self.price*buying,text)

        elif button.text() =='매도':
            selling, ok = QInputDialog.getInt(self, '매도 수량', '매도 수량을 입력하세요.')
            if selling <0 or selling>self.holding: #예외처리
                QMessageBox.warning(self, '경고!', '{}이하의 자연수를 입해주세요.'.format(self.holding), QMessageBox.Ok)
            elif ok:
                self.holding -= selling
                self.investmentamount -= self.price * selling
                # 보유금액에 증가
                text = '{} {}개 매도\n잔고: {} + {}'.format(self.itemname, selling, self.status.money, self.price*selling)
                self.status.moneyUpdate(self.price*selling,text)
            if not self.holding:
                self.investmentamount=0

        self.holdinglabel.setText('보유량: {}'.format(self.holding))
    # 그래프 기울기 관리
    def changeEconomy(self):
        random = np.random.randint(1,1001)
        if random <= 15: return True  # 1.5%
        else: return False

    def changeGradient(self):
        random= np.random.randint(1,21)
        if random<=7: return True #35%
        else: return False

    def updateEconomy(self):
        random = np.random.randint(1, 101)
        if random <= 12:       #12%
            self.economy = -10
        elif random <= 36:     # 24%
            self.economy = -4
        elif random <= 70:     #34%
            self.economy = np.random.randint(-1,2)
        elif random <= 92:    #22%
            self.economy = 6
        else:  #8%
            self.economy = 9
        print(self.economy)

    def updateGradient(self):
        self.gradient= np.random.normal(0,0.005,1)[0]+0.001* self.economy

    #
    def setAdjustment(self):
        if self.price<600 and self.gradient>0:
            self.adjustment=1.8
        elif self.price<2000 :
            self.adjustment=1.3
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

    def setSubgradient(self):
        if self.price <600:
            self.subgradient = 0.0001* np.random.randint(0,600) #무조건 오르도록 조정
        elif self.price <2000:
            self.subgradient = 0.0001* np.random.randint(-300,400) #소폭 상승하도록 조정
        else:
            self.subgradient = 0.0001* np.random.randint(-600,601) # 유지하도록 조정


    # 그래프 갱신
    def updateLine(self, i):
        # 60초가 채워지면 그래프 다시그리기
        lastx=self.x[-1]
        if lastx > self.x[0]+59:
            self.x = [0]
            self.y = [self.y[-1]]
            self.ax.set_xlim(self.x[0],self.x[0]+60)
            self.ax.set_ylim(self.y[0]*0.5, self.y[0]*1.5)
            self.ax.set_xlabel('{}: {}: {}:'.format(self.status.week,self.status.day,self.status.hour))
            self.ax.figure.canvas.draw()
        # 값 갱신

        if self.changeEconomy():
            self.updateEconomy()
        if self.changeGradient():
            self.updateGradient()
        self.setAdjustment()
        self.setSubgradient()

        x = self.x[-1] + 1
        y = int((1+self.adjustment*self.gradient+self.subgradient)*self.y[-1])

        self.x.append(x)
        self.y.append(y)

        self.line.set_data(self.x,self.y)

        # 내용 갱신
        self.price = self.y[-1]
        self.presentvalue = self.price * self.holding

        self.pricelabel.setText('매입가: {}'.format(self.price))
        self.presentvaluelabel.setText('현재가치: {}'.format(self.presentvalue))
        self.gnllabel.setText('평가손익: {}'.format(self.presentvalue - self.investmentamount))

        # 시간갱신
        if self.itemname == 'HHHH':
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

        #비트코인 생성
        vbox.addWidget(Bitcoin('HHHH',self.status))
        vbox.addWidget(Bitcoin('aaaa',self.status))
        vbox.addWidget(Bitcoin('bbbb',self.status))

        scrollarea.setWidget(bitcoins)

        mainlayout.addWidget(scrollarea)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    bcmarket = BitcoinMarket()
    bcmarket.show()
    sys.exit(app.exec_())