import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import Logic
import sqlite3
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import UI.resources.Images

id_map = 0
seed = random.randint(1, 101)


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
        self.load_window = CreateWindow(0)
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
        self.LoadMap.clicked.connect(self.open_window_ingame_1)
        self.LoadMap_2.clicked.connect(self.open_window_ingame_2)
        self.LoadMap_3.clicked.connect(self.open_window_ingame_3)
        self.Back.clicked.connect(self.open_back_window)

    def open_window_ingame_1(self):
        global id_map
        id_map = 1
        db = sqlite3.connect("MapsDb.db")
        c = db.cursor()
        if c.execute(f"SELECT MapArr FROM Maps WHERE id = {id_map}").fetchall() != "":
            db.close()
            self.ingame_window = InGameWindow_loaded()
            self.ingame_window.show()
            self.hide()
            db.close()
        else:
            db.close()

    def open_window_ingame_2(self):
        global id_map
        id_map = 2
        db = sqlite3.connect("MapsDb.db")
        c = db.cursor()
        if c.execute(f"SELECT MapArr FROM Maps WHERE id = {id_map}").fetchall() != "":
            db.close()
            self.ingame_window = InGameWindow_loaded()
            self.ingame_window.show()
            self.hide()
            db.close()
        else:
            db.close()

    def open_window_ingame_3(self):
        global id_map
        id_map = 3
        db = sqlite3.connect("MapsDb.db")
        c = db.cursor()
        if c.execute(f"SELECT MapArr FROM Maps WHERE id = {id_map}").fetchall() != "":
            db.close()
            self.ingame_window = InGameWindow_loaded()
            self.ingame_window.show()
            self.hide()
            db.close()
        else:
            db.close()

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class CreateWindow(QMainWindow):
    def __init__(self, t):
        self.t = t
        super().__init__()
        uic.loadUi('TheGodgame_Create.ui', self)
        self.setFixedSize(self.size())
        self.CreateButton.clicked.connect(self.open_window_ingame)
        self.Back.clicked.connect(self.open_back_window)
        self.CodePole.textChanged[str].connect(self.OnChanged)

    def OnChanged(self, t):
        self.t = t

    def open_window_ingame(self):
        if str(self.t) != "" and str(self.t).isdigit():
            if self.t < 256:
                self.ingame_window = InGameWindow_created()
                self.ingame_window.show()
                self.hide()

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class InGameWindow_loaded(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_InGame.ui', self)
        db = sqlite3.connect("MapsDb.db")
        c = db.cursor()
        arr = c.execute(f"SELECT MapArr FROM Maps WHERE id = {id_map}").fetchall()
        db.close()
        self.setFixedSize(self.size())
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.pill_image = arr
        self.q_image = ImageQt(self.pill_image)
        self.pixmap = QPixmap.fromImage(self.q_image)
        self.image.setPixmap(self.pixmap)

        self.Leave.clicked.connect(self.open_back_window)

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class InGameWindow_created(QMainWindow):
    def __init__(self):
        global id_map
        global seed
        super().__init__()
        uic.loadUi('TheGodgame_InGame.ui', self)
        arr = Logic.save_map(id_map)
        self.setFixedSize(self.size())
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.pill_image = arr
        self.q_image = ImageQt(self.pill_image)
        self.pixmap = QPixmap.fromImage(self.q_image)
        self.image.setPixmap(self.pixmap)

        self.Leave.clicked.connect(self.open_back_window)

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
