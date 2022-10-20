from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import Logic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import UI.resources.Images


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_main.ui', self)
        self.setFixedSize(self.size())
        self.PlayButton.clicked.connect(self.open_window_main)

    def open_window_main(self):
        self.play_window = PlayWindow()
        self.play_window.show()
        self.close()


class PlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_play.ui', self)
        self.setFixedSize(self.size())
        self.LoadMap.clicked.connect(self.open_window_load)
        self.CreateNewMap.clicked.connect(self.open_window_create)
        self.Back.clicked.connect(self.open_back_window)

    def open_window_load(self):
        self.load_window = LoadWindow()
        self.load_window.show()
        self.close()

    def open_window_create(self):
        self.load_window = CreateWindow()
        self.load_window.show()
        self.close()

    def open_back_window(self):
        self.back_window = MainWindow()
        self.back_window.show()
        self.close()


class LoadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_Load.ui', self)
        self.setFixedSize(self.size())
        self.LoadMap.clicked.connect(self.open_window_ingame)
        self.LoadMap_2.clicked.connect(self.open_window_ingame)
        self.LoadMap_3.clicked.connect(self.open_window_ingame)
        self.Back.clicked.connect(self.open_back_window)

    def open_window_ingame(self):
        self.ingame_window = InGameWindow()
        self.ingame_window.show()
        self.hide()

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class CreateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_Create.ui', self)
        self.setFixedSize(self.size())
        self.CreateButton.clicked.connect(self.open_window_ingame)
        self.Back.clicked.connect(self.open_back_window)

    def open_window_ingame(self):
        self.ingame_window = InGameWindow()
        self.ingame_window.show()
        self.hide()

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class InGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_InGame.ui', self)
        self.setFixedSize(self.size())
        a = Logic.save_map()
        print(type(a))
        self.pixmap = QPixmap(a)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.image.setPixmap(self.pixmap)
        self.Leave.clicked.connect(self.open_back_window)

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
