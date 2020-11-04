from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Button import Button

from multiprocessing import Process, Queue
import multiprocessing as mp

import time
starttime=time.time()

def producer(q):
    proc = mp.current_process()
    print(proc.name)

    while 1:
        currenttime = time.time() - starttime
        time.sleep(1)
        data = '{}'.format(int(currenttime))
        q.put(data)

class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self,q):
        super().__init__()
        self.q = q

    def run(self):
        while 1:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)

q = Queue()

p = Process(name='producer', target=producer, args=(q,), daemon=True)
p.start()


class Status(QWidget):
    def __init__(self,q,parent=None):
        super().__init__(parent)
        self.money=0

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.timeUpdate)
        self.consumer.start()

        self.setUI()


    def setUI(self):
        mainlayout = QHBoxLayout()
        self.setLayout(mainlayout)

        self.currentmoney = QLabel('Money: {}'.format(self.money))
        self.currenttime = QLabel('시간 경과: {}m'.format(0))

        mainlayout.addWidget(Button('save data', self.buttonClicked))
        mainlayout.addStretch(2)
        mainlayout.addWidget(self.currentmoney)
        mainlayout.addStretch(1)
        mainlayout.addWidget(self.currenttime)


    def buttonClicked(self):
        button = self.sender()

        self.money += 100
        print(self.money)
        self.currentmoney.setText('Money: {}'.format(self.money))
        self.currentmoney.repaint()

    def timeUpdate(self,data):
        self.currenttime.setText('시간 경과: {}m'.format(data))
        self.currenttime.repaint()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    status = Status(q)
    status.show()
    sys.exit(app.exec_())