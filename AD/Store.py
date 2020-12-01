from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Button import Button

class Store(QWidget):

    def __init__(self, status):
        super().__init__()
        self.status = status
        self.setUI()



    def setUI(self):
        mainlayout = QVBoxLayout()
        tablayout = QVBoxLayout()
        itemlayout = QGridLayout()

        self.setLayout(mainlayout)
        mainlayout.addWidget(QLabel('원하시는 상품을 구매하세요. '))
        mainlayout.addLayout(tablayout)
        mainlayout.addLayout(itemlayout)
        # 탭
        tab = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab, '색상')

        tablayout.addWidget(tabs)

        #색상
        tab.layout = QGridLayout()

        self.redButton = Button("Red", self.buttonClicked)
        self.yellowButton = Button("Yellow", self.buttonClicked)
        self.blueButton = Button("Blue", self.buttonClicked)
        self.greenButton = Button("Green", self.buttonClicked)
        self.orangeButton = Button("Orange", self.buttonClicked)
        self.purpleButton = Button("Purple", self.buttonClicked)
        self.brownButton = Button("Brown", self.buttonClicked)
        self.cyanButton = Button("Cyan", self.buttonClicked)
        self.skyblueButton = Button("Skyblue", self.buttonClicked)

        self.colorButton_list = ["Red", "Yellow", "Blue", "Green", "Orange", "Purple", "Brown", "Cyan", "Skyblue"]
        self.colorButton_dic = {"Red": self.redButton, "Yellow": self.yellowButton, "Blue": self.blueButton,
                                "Green": self.greenButton, "Orange": self.orangeButton, "Purple": self.purpleButton,
                                "Brown": self.brownButton, "Cyan": self.cyanButton, "Skyblue": self.skyblueButton}
        self.RGBNumber_dic = {"Red": (255, 0, 0), "Yellow": (255, 228, 0), "Blue": (0, 0, 255),
                              "Green": (0, 255, 0), "Orange": (255, 94, 0), "Purple": (217, 65, 197),
                              "Brown": (165, 42, 42), "Cyan": (0, 255, 255), "Skyblue": (135, 206, 250)}

        button_list = [self.redButton, self.yellowButton, self.blueButton, self.greenButton,
                       self.orangeButton, self.purpleButton, self.brownButton, self.cyanButton,
                       self.skyblueButton]

        # button 생성
        r = 0;
        c = 0
        for i in button_list:
            i.setStyleSheet('background:gray')
            tab.layout.addWidget(i, r, c)
            c += 1
            if c > 2:
                r += 1;
                c = 0

        self.color_price = 10000
        self.count = 2
        # 데이터 불러오기
        for key in list(self.status.data['brushcolors'].keys()):
            if key!='Black':
                self.colorButton_dic[key].setStyleSheet('background:%s' % key)
                self.colorButton_dic[key].setEnabled(False)
                self.moneyChange()

        tab.setLayout(tab.layout)

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key in self.colorButton_list:
            reply = QMessageBox.question(self, "구매", "구입하시겠습니까?\n{:,}".format(self.color_price),
                                         QMessageBox.No | QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.status.money < self.color_price:
                    QMessageBox.warning(self, "경고", "잔액이 부족합니다.", QMessageBox.Ok)
                else:
                    self.colorButton_dic[key].setStyleSheet('background:%s' %key)
                    self.colorButton_dic[key].setEnabled(False)
                    self.status.moneyUpdate(-self.color_price, "{}구입\n{:,} - {:,}".format(key, self.status.money, self.color_price))
                    self.status.current_brush_color["{}".format(key)] = self.RGBNumber_dic[key]
                    self.status.cb.addItem("{}".format(key))
                    self.moneyChange()
                    # 파산체크
                    if self.status.bankrupt():
                        self.status.defeat()
                self.status.showAchievement() # 모든 색상을 구입했는지 판단
            else:
                pass

    def moneyChange(self):
        self.color_price = self.color_price * (self.count ** 2)
        self.count += 1


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    store = Store()
    store.show()
    sys.exit(app.exec_())

