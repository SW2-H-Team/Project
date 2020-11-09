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

timereference = []
moneyreference = []

class Bitcoin(QWidget):
    def __init__(self,name,status):
        super().__init__()

        self.status=status

        self.x = [0]
        self.y = [random.randint(700, 1000)]

        self.weigth = 1  # 가중치

        self.fig = Figure(figsize=(5, 2))
        self.ax = self.fig.add_subplot(ylim=(self.y[0] * 0.9 - 200, self.y[0] * 1.1 + 200), xlim=(0, 60))
        self.canvas = FigureCanvas(self.fig)

        self.line, = self.ax.plot(self.x, self.y,color='red', animated=True, lw=1)

        self.name = name        #종목이름
        self.price = random.randint(700,1000) #매입가
        self.holding=0          #보유량

        self.investmentamount = 0 # 총 투자금액
        self.presentvalue = self.price*self.holding # 현재 보유중인 코인의 가치



        self.setUI()
        self.ani = animation.FuncAnimation(self.fig, self.update_line, blit=True, interval=1000)

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

        rightlayout.addWidget(QLabel(self.name), 0, 0)
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
                    self.status.moneyUpdate(-1*self.price*buying)

        elif button.text() =='매도':
            selling, ok = QInputDialog.getInt(self, '매도 수량', '매도 수량을 입력하세요.')
            if selling <0 or selling>self.holding: #예외처리
                QMessageBox.warning(self, '경고!', '{}이하의 자연수를 입해주세요.'.format(self.holding), QMessageBox.Ok)
            elif ok:
                self.holding -= selling
                self.investmentamount -= self.price * selling
                # 보유금액에 증가
                self.status.moneyUpdate(self.price*selling)

        self.holdinglabel.setText('보유량: {}'.format(self.holding))

    # 그래프 갱신
    def update_line(self, i):

        lastx=self.x[-1]
        if lastx > self.x[0]+59:
            self.x = [self.x[-1]]
            self.y = [self.y[-1]]
            self.ax.set_xlim(self.x[0],self.x[0]+60)
            self.ax.set_ylim(self.y[0]*0.9-200, self.y[0]*1.1+200)
            self.ax.figure.canvas.draw()

        x = self.x[-1] + 1
        y = self.y[-1]+random.randint(-8, 10)

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
        if self.name == 'HHHH':
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