from PyQt5.QtWidgets import *

class Button(QToolButton):
    """
    이 게임에 존재하는 버튼을 만드는 클래스입니다.
    콜백함수를 받아 버튼을 누를 때 기능하게 합니다.
    """
    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)