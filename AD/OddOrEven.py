from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Button import Button

import numpy as np


class OddOrEven(QWidget):
    def __init__(self,status):
        super().__init__()
        self.status=status

        self.charge=self.status.data['ore'][0]
        self.history =self.status.data['ore'][1]

        self.setUI()

    # 인터페이스 설정
    def setUI(self):
        #레이아웃
        mainlayout = QVBoxLayout()
        historylayout = QGridLayout()
        buttonlayout = QHBoxLayout()
        statuslayout = QHBoxLayout()
        charginglayout = QHBoxLayout()

        self.setLayout(mainlayout)
        mainlayout.addStretch(1)
        mainlayout.addLayout(historylayout)
        mainlayout.addStretch(2)
        mainlayout.addLayout(buttonlayout)
        mainlayout.addStretch(2)
        mainlayout.addLayout(statuslayout)
        mainlayout.addStretch(2)
        mainlayout.addLayout(charginglayout)
        mainlayout.addStretch(1)

        #히스토리레이아웃

        self.historylabel = QLabel(self.history)
        historylayout.addWidget(QLabel('기록'),2,4,2,8)
        historylayout.addWidget(self.historylabel,4,4,4,8)

        #버튼레이아웃
        self.oddbutton = Button('홀',self.buttonClicked)
        self.evenbutton = Button('짝',self.buttonClicked)

        self.oddbutton.setCheckable(True)
        self.evenbutton.setCheckable(True)

        buttonlayout.addStretch(2)
        buttonlayout.addWidget(self.oddbutton)
        buttonlayout.addStretch(1)
        buttonlayout.addWidget(self.evenbutton)
        buttonlayout.addStretch(2)

        #상태레이아웃
        status=''
        self.statuslabel=QLabel(status)

        statuslayout.addWidget(self.statuslabel)

        #충전레이아웃

        self.chargelabel = QLabel(str(self.charge))
        chargebutton = Button('충전하기', self.buttonClicked)
        withdrawlbutton = Button('출금하기',self.buttonClicked)

        charginglayout.addStretch(1)
        charginglayout.addWidget(self.chargelabel)
        charginglayout.addWidget(chargebutton)
        charginglayout.addWidget(withdrawlbutton)
        charginglayout.addStretch(1)

    # 상태메세지 바꾸기
    def statusUpdate(self,text):
        self.statuslabel.setText(text)

    def chargeUpdate(self,amount):
        self.charge+=amount
        self.chargelabel.setText('{:,}'.format(self.charge))

    # 한 시간마다 결과나옴.
    def getNumber(self):
        number = np.random.randint(1,3)
        self.historyUpdate(number) #결과 나올때마다 기록 업데이트
        # 결과 확인
        self.checkResult(number)

    def checkResult(self,number):
        # 버튼을 선택했을때,
        if self.oddbutton.isChecked() or self.evenbutton.isChecked():
            if number==1:
                if self.oddbutton.isChecked():
                    self.statusUpdate('성공! {:,}원 획득! '.format(int(1.9 * self.charge)))
                    self.chargeUpdate(int(0.9*self.charge))
                    self.oddbutton.toggle()
                else:
                    self.statusUpdate('실패! {:,}원 증발'.format(self.charge))
                    self.chargeUpdate(-self.charge)
                    self.evenbutton.toggle()
                    #파산체크
                    self.status.checkDefeated()
            elif number==2:
                if self.oddbutton.isChecked():
                    self.statusUpdate('실패! {:,}원 증발'.format(self.charge))
                    self.chargeUpdate(-self.charge)
                    self.oddbutton.toggle()
                    #파산체
                    self.status.checkDefeated()
                else:
                    self.statusUpdate('성공! {:,}원 획득! '.format(int(1.9 * self.charge)))
                    self.chargeUpdate(int(0.9*self.charge))
                    self.evenbutton.toggle()
        # 어떤 버튼도 선택되지 않을 때,
        else:
            pass
            #self.statusUpdate('홀?짝?')

    # 기록 업데이트
    def historyUpdate(self,number):
        if len(self.history)==48: #하루가 지나면 기록 초기화
            self.history=''
        result= '홀'if number==1 else '짝'
        self.history+=result+' '
        self.historylabel.setText(self.history)

    def buttonClicked(self):
        button= self.sender()
        # 충전 버튼
        if button.text()=='충전하기' :
            charge, ok = QInputDialog.getInt(self, '충전하기', '충전할 금액을 입력하세요.\n충전가능금액: {:,}'
                                             .format(self.status.money))
            # ok 버튼을 누르면,
            if ok:
                # 예외처리
                if charge <= 0:
                    QMessageBox.warning(self, '경고!', '0보다 큰 값을 입력해 주세요.', QMessageBox.Ok)
                elif charge > self.status.money:
                    QMessageBox.warning(self, '경고!', '최대 보유금액 만큼의 값을 입력할 수 있습니다.', QMessageBox.Ok)
                # 정상작동
                else:
                    self.chargeUpdate(charge)
                    text= '홀짝게임에 충전\n잔고: {:,} - {:,}'.format(self.status.money,charge)
                    self.status.moneyUpdate(-charge,text)

        elif button.text()=='출금하기' :
            withdrawl, ok = QInputDialog.getInt(self, '출금하기', '출금할 금액을 입력하세요.\n수수료 10%\n출금가능금액: {}'
                                             .format(self.charge))
            # ok버튼을 누르면,
            if ok:
                # 예외처리
                if withdrawl <=0:
                    QMessageBox.warning(self, '경고!', '0보다 큰 값을 입력해 주세요.', QMessageBox.Ok)
                elif withdrawl >self.charge:
                    QMessageBox.warning(self, '경고!', '최대 충전금액 만큼의 값을 입력할 수 있습니다.', QMessageBox.Ok)
                # 정상작동
                else:
                    self.chargeUpdate(-withdrawl)
                    text= '홀짝게임에서 출금\n잔고: {:,} + {:,}'.format(self.status.money,int(0.9*withdrawl))
                    self.status.moneyUpdate(int(0.9*withdrawl),text)
                    self.status.showAchievement()

        # 홀 선택
        elif len(button.text())==1:
            if not self.charge:
                button.toggle()
                QMessageBox.warning(self, '경고!', '입금부터 하세요.',QMessageBox.Ok)

            elif button.text()=='홀':
                if button.isChecked():
                    if self.evenbutton.isChecked(): # 다른 버튼이 눌려져있다면 취소
                        self.evenbutton.toggle()
                    self.statusUpdate('홀을 선택했습니다.')
                elif not button.isChecked():
                    self.statusUpdate('홀 선택을 취소했습니다.')

            # 짝 선택
            elif button.text()=='짝':
                if button.isChecked():
                    if self.oddbutton.isChecked(): # 다른 버튼이 눌려져있다면 취소
                        self.oddbutton.toggle()
                    self.statusUpdate('짝을 선택했습니다.')
                elif not button.isChecked():
                    self.statusUpdate('짝 선택을 취소했습니다.')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ore = OddOrEven()
    ore.show()
    sys.exit(app.exec_())
