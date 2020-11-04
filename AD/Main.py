from PyQt5.QtWidgets import *

from Status import *
from Painter import Painter
from Store import Store
from Button import Button

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 탭 레이아웃
        tab1 = Painter()
        tab2 = Store()
        tab3 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, '그림그리기')
        tabs.addTab(tab2, '상점')
        tabs.addTab(tab3, '용돈벌기')

        tablayout = QVBoxLayout()
        tablayout.addWidget(tabs)

        #상태창
        status = Status(q)

        # 메인 레이아웃
        mainlayout = QVBoxLayout()
        mainlayout.addLayout(tablayout)
        mainlayout.addWidget(status)

        self.setLayout(mainlayout)
        self.setWindowTitle('AD')
        self.setGeometry(300, 150, 700, 500)
        self.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())