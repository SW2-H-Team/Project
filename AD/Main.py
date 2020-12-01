import pickle
import numpy as np

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

        # 제목
        gametitle = QLabel('    Dream Of Painter')
        gametitlefont=QFont('Chilanka',30)
        gametitlefont.setBold(True)
        gametitle.setFont(gametitlefont)
        gametitle.setFixedSize(400,50)

        # 설명
        story="""
         화가인 당신은 찢어지게 가난하여 늘 생활고에 시달렸습니다.
        결국 벼랑 끝에 몰린 심정으로 사채를 빌렸는데...
        하지만 그동안 밀린 월세, 공과금 등을 지불하고 남은 돈은 단 5만원 뿐.
        절망스럽지만 여기서 인생을 포기할 순 없습니다. 
        어떻게든 빚을 갚고 물감을 구입하여 인생의 역작을 완성하세요!
        """
        storylabel = QLabel(story)
        storyfont=QFont('Noto Serif CJK KR ExtraLight',10)
        storyfont.setItalic(True)
        storylabel.setFont(storyfont)
        storylabel.setFixedSize(500,150)

        # 이름입력칸
        self.nameinput = QLineEdit()
        self.nameinput.setFixedSize(200,50)
        self.nameinput.setMaxLength(10)
        self.nameinput.setStyleSheet('font: 15pt "Noto Sans CJK HK Medium";' )

        # 입력버튼
        inputbutton = Button('로그인',self.buttonClicked)
        #inputbutton.setFixedSize(100,50)

        #배치
        mainlayout.addWidget(gametitle,0,0)
        mainlayout.addWidget(storylabel,1,0)
        mainlayout.addWidget(self.nameinput,5,4)
        mainlayout.addWidget(inputbutton,5,5)

        self.setWindowTitle('로그인하세요.')
        self.setFixedSize(600,400)
        self.move(200, 120)
        self.show()

    def buttonClicked(self):
        button = self.sender()
        if button.text()=='로그인':
            # 현재 입력창의 텍스트를 이름으로 설정,
            name = self.nameinput.text()
            # 아무것도 입력되지 않으면,
            if len(name)==0:
                QMessageBox.warning(self, '경고!', '뭐라도 입력하세요.', QMessageBox.Ok)
            # 입력되면,
            else:
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

        # 기록표시
        recordfont=QFont('Noto Sans CJK SC Medium',13)
        namelabel=QLabel('이름: '+self.name,)
        timelabel=QLabel('생존시간: {}주 {}일 {}시간 {}분'.format(self.time[0],self.time[1],self.time[2],self.time[3]))
        peakofmoneylabel=QLabel('최고 보유금액: {:,}'.format(self.peakofmoney))

        namelabel.setFont(recordfont)
        timelabel.setFont(recordfont)
        peakofmoneylabel.setFont(recordfont)

        recordlayout.addWidget(namelabel)
        recordlayout.addWidget(timelabel)
        recordlayout.addWidget(peakofmoneylabel)

        # 파산메세지
        bankruptlabel = QLabel('파 산')
        bankruptfont=QFont('Noto Sans CJK HK Black',100)
        bankruptfont.setBold(True)
        bankruptlabel.setFont(bankruptfont)
        bankruptlabel.setAlignment(Qt.AlignCenter)

        # 재시도
        retrylabel = QLabel('다시하시겠습니까?                               ')
        retrybutton=Button('다시하기',self.buttonClicked)
        retrybutton.setFixedSize(200,40)

        retrylayout.addWidget(retrylabel,alignment=Qt.AlignRight)
        retrylayout.addWidget(retrybutton,alignment=Qt.AlignRight)

        # 레이아웃
        self.setLayout(mainlayout)
        mainlayout.addLayout(recordlayout)
        mainlayout.addWidget(bankruptlabel)
        mainlayout.addStretch()
        mainlayout.addLayout(retrylayout)

        self.setStyleSheet('background-color: rgb(33, 33, 33);' 'color: rgb(255, 255, 255);')
        self.setWindowTitle('파산했습니다.')
        self.setFixedSize(600, 400)
        self.move(200, 120)

        self.show()

    def buttonClicked(self):
        button=self.sender()
        if button.text()=='다시하기':
            self.close()
            self.ex = LoginWindow()

#업적달성창
class AchievementWindow(QWidget):
    def __init__(self,achievement,record,totalrecord):
        super().__init__()

        self.achievement=achievement
        self.record=record
        self.totalrecord=totalrecord

        self.setUI()

    def setUI(self):
        #레이아웃
        mainlayout=QVBoxLayout()
        labellayout=QVBoxLayout()
        recordlayout=QVBoxLayout()
        buttonlayout=QHBoxLayout()

        self.setLayout(mainlayout)
        mainlayout.addLayout(labellayout)
        mainlayout.addStretch()
        mainlayout.addLayout(recordlayout)
        mainlayout.addStretch()
        mainlayout.addLayout(buttonlayout)

        self.setWindowTitle('업적달성!')
        self.setFixedWidth(600)
        self.move(200, 120)

        self.show()

        #라벨
        if str(self.achievement).isdecimal():
            achievementlabel=QLabel('{:,}원 달성!'.format(self.achievement))
        else:
            achievementlabel =QLabel('All-Color 달성!')
        achievementfont=QFont('Noto Sans CJK SC Black',23)
        achievementfont.setBold(True)
        achievementlabel.setFont(achievementfont)
        labellayout.addWidget(achievementlabel)

        #기록표시
        myrecord=QLabel('당신의 기록 : {}:{}:{}:{}'.format(self.record[0],self.record[1],self.record[2],self.record[3]))
        font0=QFont('궁서',18)
        font0.setItalic(True)
        myrecord.setFont(font0)
        recordlabel1=QLabel('해당 업적 최단기간 달성 순위표')
        font1=QFont('돋움',10)
        font1.setBold(True)
        recordlabel1.setFont(font1)
        recordlabel2=QLabel('순위\t\t이름\t\t\t기록')
        self.records=QTextEdit()
        self.records.setReadOnly(True)
        self.records.setFixedHeight(200)

        self.showRank(self.totalrecord)

        recordlayout.addWidget(myrecord)
        recordlayout.addStretch()
        recordlayout.addWidget(recordlabel1)
        recordlayout.addStretch()
        recordlayout.addWidget(recordlabel2)
        recordlayout.addWidget(self.records)

        #버튼
        continuebutton=Button('계속하기',self.buttonClicked)

        buttonlayout.addWidget(continuebutton)

    def showRank(self,totalrecord):
        records=totalrecord

        for num,i in enumerate(records):
            self.records.append('{}.\t{}\t\t{}:{}:{}:{}'.format(num+1,i[0],i[1][0],i[1][1],i[1][2],i[1][3]))


    def buttonClicked(self):
        button=self.sender()
        if button.text()=='계속하기':
            self.close()

# 게임화면
class MyApp(QWidget):
    def __init__(self,name):
        super().__init__()
        # 데이터초기화
        self.totaldata={}
        self.data={'playername':name,'time':[0,6,19,0],'pom':50000,'money':60000,'debt':200000000,'history':'',
                   'bitcoins':[],'ore':[0,''],'brushcolors':{"Black": (0, 0, 0)},
                   'already':[False,False,False,False,False,False]}

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
	    # 보유색상
        self.current_brush_color = self.data['brushcolors']

        # 업적달성현황
        self.already108=self.data['already'][0]
        self.already1010=self.data['already'][1]
        self.already1012=self.data['already'][2]
        self.already1016=self.data['already'][3]
        self.already1020=self.data['already'][4]
        self.alreadyac=self.data['already'][5]

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
                    # 해당 이름의 데이터를 불러올기 결정하기
                    reply = QMessageBox.information(self, ' ', '해당 이름의 데이터가 존재합니다. 이어하겠습니다.',
                                                 QMessageBox.Yes , QMessageBox.Yes)
                    self.data = totaldata[name]  # 데이터를 덮어씌우기
                # 없으면,
                else:
                    totaldata[name] = self.data  # 사전에 새로운 이름에 대한 정보 추가,
                # 그리고 변수에 이 데이터를 저장
                self.totaldata = totaldata
            except:
                pass
            f.close()

        except:
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
        #홀짝게임정보
        self.data['ore']=[self.getmoneytab.tab2.charge,self.getmoneytab.tab2.history]
        # 보유색상, 구매현황
        self.data['brushcolors']=self.current_brush_color
        # 최고 보유금액
        self.data['pom']=self.peakofmoney
        # 업적성취 정보
        self.data['already'][0]=self.already108
        self.data['already'][1]=self.already1010
        self.data['already'][2]=self.already1012
        self.data['already'][3]=self.already1016
        self.data['already'][4]=self.already1020
        self.data['already'][5]=self.alreadyac
        # 총데이터 저장
        self.totaldata[self.playername]=self.data
        f = open('data.dat', 'wb')
        pickle.dump(self.totaldata, f)
        f.close()
        #그림저장
        self.paintertab.canvas.image.save("pictures/{}_main_image.png".format(self.playername))

    # 업적달성시 기록저장을 위해 데이터를 불러오기
    def recordLoad(self):
        try:
            f = open('record.dat', 'rb')
            # 데이터에 불러온 기록을 저장
            totalrecord = pickle.load(f)
            # 그리고 변수에 이 데이터를 저장
            self.totalrecord = totalrecord
            f.close()
            return totalrecord
        except:
            return {10**8:[],10**10:[],10**12:[],10**16:[],10**20:[],'allcolor':[]}

    # 기록 정렬
    def recordSort(self,totalrecord,achievement):
        before=totalrecord[achievement]
        after=sorted(before,key=lambda x: (x[1][0],x[1][1],x[1][1],x[1][2],x[1][3]))[:10]
        totalrecord[achievement]=after
        return totalrecord

    # 업적달성시 기록저장
    def recordSaveNReturn(self,achievement,record):
        #파일에서 해당 업적의 기록들을 꺼내와 자신의 기록과 합침
        totalrecord = self.recordLoad()
        myrecord = [self.playername,record]
        totalrecord[achievement].append(myrecord)
        #합친 기록을 정렬
        totalrecord=self.recordSort(totalrecord,achievement)
        #파일에 합친 기록을 저장
        f = open('record.dat', 'wb')
        pickle.dump(totalrecord, f)
        f.close()
        #리턴
        return totalrecord[achievement]

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
        self.moneylabel = QLabel('Money: {:,}원'.format(self.money))
        self.timelabel = QLabel('시간 경과: {}m'.format(self.time[3]))
        self.timelabel.setFixedWidth(200)

        statuslayout.addWidget(Button('데이터 저장', self.buttonClicked))
        statuslayout.addStretch(1)
        statuslayout.addWidget(self.namelabel)
        statuslayout.addStretch(1)
        statuslayout.addWidget(self.moneylabel)
        statuslayout.addStretch(1)
        statuslayout.addWidget(self.timelabel)

        # 가계부
        self.historylabel = QLabel('가계부\t\t남은 빚: {:,}'.format(self.debt))
        self.history = QTextEdit()
        self.history.setText(self.data['history'])
        self.history.setReadOnly(True)
        self.history.setFixedWidth(200)

        historylayout.addWidget(self.historylabel)
        historylayout.addWidget(self.history)



        self.setLayout(mainlayout)
        self.setWindowTitle('AD')

        self.setFixedSize(1000, 600)
        self.move(200, 100)

        self.show()

    # 모든 경제활동에서 발생하는 돈의 흐름
    def moneyUpdate(self,money,text):
        # 지출/수입 반영
        self.money += money
        self.moneylabel.setText('Money: {:,}원'.format(self.money))

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
        self.history.append('= {:,}원'.format(self.money)) #결과금액 표시
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
                # 파산체크
                if self.bankrupt():
                    self.defeat()

        self.timelabel.setText('시간 경과: {}주 {}일 {}시간 {}분'.format(self.time[0],self.time[1],self.time[2],self.time[3]))

    # 채무 상환
    def payBack(self):
        self.debt -= 1000000
        self.historylabel.setText('가계부\t\t남은 빚: {}'.format(self.debt))
        if self.money >= 1000000:
            text = '채무 상환\n잔고: {:,} - {:,}'.format(self.money, 1000000)
            self.moneyUpdate(-1000000,text)
        else:
            # 구입한 색깔이 있으면 해당 색깔을 압류함.
            if len(self.current_brush_color) !=1:
                color=self.foreclosure()
                text = '{} 압류당함.\n잔고: {} - {}'.format(color, self.money, self.money)
                self.moneyUpdate(-self.money, text)
            #없으면 패배처리.
            else:
                QMessageBox.warning(self, '파산!', '모든 것을 압류당했습니다!',QMessageBox.Ok)
                self.defeat()

    # 색깔 압류
    def foreclosure(self):
        index=np.random.randint(1,len(self.current_brush_color))
        color=self.cb.itemText(index)
        # 잠겼던 버튼 다시 해제
        self.storetab.colorButton_dic[color].setEnabled(True)
        self.storetab.colorButton_dic[color].setStyleSheet('background:gray')
        del self.current_brush_color[color] # 보유색상에서 제거
        self.cb.removeItem(index) #콤보박스에서도 제거
        return color #압류한 색상 리턴,

    # 패배 처리
    def defeat(self):
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

    # 업적달성창 띄우기
    def showAchievement(self):
        achievement=self.achievement()
        if achievement:
            self.dataSave()
            myrecord=[self.time[0],self.time[1],self.time[2],self.time[3]]
            totalrecord=self.recordSaveNReturn(achievement,myrecord)
            self.ex=AchievementWindow(achievement,myrecord,totalrecord)

    # 업적달성
    def achievement(self):
        if self.money>=10**8 and not self.already108: #1억
            self.already108=True
            return 10**8
        elif self.money >= 10**10 and not self.already1010: #100억
            self.already1010=True
            return 10**10
        elif self.money >= 10**12 and not self.already1012: #1조
            self.already1012=True
            return 10**12
        elif self.money >= 10**16 and not self.already1016: #1경
            self.already1016=True
            return 10**16
        elif self.money >= 10**20 and not self.already1020: #1해
            self.already1020=True
            return 10**20
        elif len(self.current_brush_color)==len(self.storetab.colorButton_list)+1: # 모든 색상 구입
            return 'allcolor'
        else:
            return 0
    ###################################################
    def buttonClicked(self):
        button = self.sender()

        if button.text()=='데이터 저장':
            reply = QMessageBox.question(self, '저장하기', '지금까지의 데이터를 저장하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.dataSave()
                ok = QMessageBox.question(self, '저장됨', '데이터를 성공적으로 저장했습니다!',
                                          QMessageBox.Yes, QMessageBox.Yes)


############################################
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    ex = LoginWindow()
    sys.exit(app.exec_())
