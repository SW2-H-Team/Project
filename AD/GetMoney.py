from PyQt5.QtWidgets import *

from Bitcoin import *
from OddOrEven import *

#용돈벌기 탭
class GetMoney(QWidget):
    """
    돈을 벌 수 있는 '비트코인'과 '홀짝게임'이 존재하는 탭입니다.
    희망하는 방법으로 돈을 벌 수 있습니다.
    """
    def __init__(self,status):
        super().__init__()

        self.status=status

        self.setUI()

    # UI설정
    def setUI(self):
        mainlayout=QVBoxLayout()
        tablayout = QHBoxLayout()

        self.setLayout(mainlayout)
        mainlayout.addLayout(tablayout)
        # 탭
        self.tab1=BitcoinMarket(self.status)
        self.tab2=OddOrEven(self.status)

        tabs = QTabWidget()
        tabs.addTab(self.tab1, '비트코인')
        tabs.addTab(self.tab2, '홀짝')

        tablayout.addWidget(tabs)