import sys, os, random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import random

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(211, xlim=(0, 50), ylim=(50, 100))
        self.axes.set_xlabel('fffffff')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

class AnimationWidget(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        vbox = QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=10, height=8, dpi=100)

        vbox.addWidget(self.canvas)      #캔버스

        hbox = QHBoxLayout()                   # 버튼있는 레이아웃
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.x = np.arange(50)
        self.y = np.ones(50, dtype=np.float)*np.nan
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=2)

    def update_line(self,i):

        y = random.randint(70,100)
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]         #그래프 갱신
        self.line.set_ydata(new_y)

        # self.line.set_ydata(y)
        print(self.x,self.y)
        return [self.line]

    def on_start(self):
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line, blit=True, interval=100)

    def on_stop(self):
        self.ani._stop()

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())