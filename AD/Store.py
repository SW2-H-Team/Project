from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button

class Store(QWidget):

    def __init__(self):
        super().__init__()
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
        tab1 = QWidget()
        tab2 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, '도구')
        tabs.addTab(tab2, '색상')

        tablayout.addWidget(tabs)

        #도구
        tab1.layout = QGridLayout()
        #색상
        tab2.layout = QGridLayout()

        self.redButton = Button("Red", self.buttonClicked)

        self.yellowButton = Button("Yellow", self.buttonClicked)
        self.blueButton = Button("Blue", self.buttonClicked)
        self.greenButton = Button("Green", self.buttonClicked)

        button_list = [self.redButton, self.yellowButton, self.blueButton, self.greenButton]

        #button 생성
        r = 0; c = 0
        for i in button_list:
            i.setStyleSheet('background:gray')
            tab2.layout.addWidget(i, r, c)
            c += 1
            if c > 1:
                r += 1; c = 0

        tab2.setLayout(tab2.layout)


    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        colorButton_list = ["Red", "Yellow", "Blue", "Green"]
        colorButton_dic = {"Red": self.redButton, "Yellow": self.yellowButton, "Blue": self.blueButton, "Green": self.greenButton}
        if key in colorButton_list:
            reply = QMessageBox.question(self, "구매", "구입하시겠습니까?",
                                         QMessageBox.No | QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                colorButton_dic[key].setStyleSheet('background:%s' %key)
                colorButton_dic[key].setEnabled(False)
            else:
                pass


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    store = Store()
    store.show()
    sys.exit(app.exec_())

