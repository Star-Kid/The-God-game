import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import Logic
import sqlite3
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import UI.resources.Images

# region glogal
id_map = 0
seed = 100
octaves = 6
lacunarity = 2
scale = 100


# endregion

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
    global seed, octaves, lacunarity, scale

    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_Create.ui', self)
        self.setFixedSize(self.size())
        self.CreateButton.clicked.connect(self.open_window_ingame)
        self.Back.clicked.connect(self.open_back_window)
        self.CodePole.textChanged[str].connect(self.OnChangedSeed)
        self.ScalePole.textChanged[str].connect(self.OnChangedScale)
        self.WaveSlider.valueChanged[int].connect(self.changeValuelacunarity)
        self.OctavesSlider.valueChanged[int].connect(self.changeValueOctaves)

    def changeValueOctaves(self, value):
        global octaves
        if value == 0:
            octaves = 4
        elif value > 0 and value <= 25:
            octaves = 5
        elif value > 25 and value < 50:
            octaves = 6
        elif value > 50 and value < 75:
            octaves = 7
        else:
            octaves = 8

    def changeValuelacunarity(self, value):
        global lacunarity
        lacunarity = round(1 + 0.02 * value, 1)

    def OnChangedSeed(self, sd):
        global seed
        seed = sd

    def OnChangedScale(self, se):
        global scale
        scale = se

    def open_window_ingame(self):
        if str(seed) != "" and str(seed).isdigit() and str(scale) != "" and str(scale).isdigit():
            if int(seed) <= 256 and 50 <= scale <= 200:
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
        arr = Logic.save_map(id_map, int(seed), int(octaves), lacunarity, int(scale))
        self.setFixedSize(self.size())
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.pill_image = arr
        self.q_image = ImageQt(self.pill_image)
        self.pixmap = QPixmap.fromImage(self.q_image)
        self.image.setPixmap(self.pixmap)
        self.Leave_btn = QPushButton('Leave', self)
        self.Leave_btn.setStyleSheet("""
                            font: 75 20pt "Arial";
                            background-color: rgb(120, 120, 120);
                    	    border: none;
                    	    padding-top: 5px;
                    	    border-radius: 25px;""")

        self.Leave_btn.resize(121, 51)
        self.Leave_btn.move(760, 20)

        self.Leave_btn.clicked.connect(self.open_back_window)

    def open_back_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()


class InGameWindow_created(QMainWindow):
    global seed, octaves, lacunarity, scale

    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_InGame.ui', self)
        arr = Logic.save_map(id_map, int(seed), int(octaves), lacunarity, int(scale))
        self.setFixedSize(self.size())
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.pill_image = arr
        self.q_image = ImageQt(self.pill_image)
        self.pixmap = QPixmap.fromImage(self.q_image)
        self.image.setPixmap(self.pixmap)
        # region register save and veave buttons
        self.Leave_btn = QPushButton('Leave', self)
        self.Leave_btn.setStyleSheet("""
                    font: 75 20pt "Arial";
                    background-color: rgb(120, 120, 120);
            	    border: none;
            	    padding-top: 5px;
            	    border-radius: 25px;""")

        self.Leave_btn.resize(121, 51)
        self.Leave_btn.move(760, 20)

        self.Save_btn = QPushButton('Save', self)
        self.Save_btn.setStyleSheet("""
                            font: 75 20pt "Arial";
                            background-color: rgb(120, 120, 120);
                    	    border: none;
                    	    padding-top: 5px;
                    	    border-radius: 25px;""")

        self.Save_btn.resize(121, 51)
        self.Save_btn.move(620, 20)
        # endregion
        self.Leave_btn.clicked.connect(self.open_leave_window)
        self.Save_btn.clicked.connect(self.open_save_window)

    def open_leave_window(self):
        self.back_window = PlayWindow()
        self.back_window.show()
        self.close()

    def open_save_window(self):
        self.save_window = SaveWindow()
        self.save_window.show()
        self.close()


class SaveWindow(QMainWindow):
    global seed, octaves, lacunarity, scale

    def __init__(self):
        super().__init__()
        uic.loadUi('TheGodgame_Save.ui', self)
        self.setFixedSize(self.size())
        self.Back.clicked.connect(self.open_back_window)
        self.Save1.clicked.connect(self.save_id)
        self.Save2.clicked.connect(self.save_id2)
        self.Save3.clicked.connect(self.save_id3)

    def save_id(self):
        global id_map
        id_map = 1
        self.save()

    def save_id2(self):
        global id_map
        id_map = 2
        self.save()

    def save_id3(self):
        global id_map
        id_map = 3
        self.save()

    def save(self):
        db = sqlite3.connect("MapsDb.db")
        c = db.cursor()
        request = str(c.execute(f"SELECT MapArr FROM Maps WHERE id = {id_map}").fetchall())[3:-4]
        if request == "null":
            nums = [seed, octaves, lacunarity, scale]
            c.execute(f"UPDATE Maps SET MapArr = ? WHERE id = ?", (str(nums), id_map))
            db.commit()
            db.close()
            f = open(f"MapsFolder/Map{id_map}.txt", "w")
            f.write(str(nums))
            f.close()
        else:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Resave")
            self.msg.setText("Do you realy want to resave this picture?")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.saveORnot)
            self.msg.exec_()

    def saveORnot(self, msg):
        if msg.text() == "Ok":
            db = sqlite3.connect("MapsDb.db")
            nums = [seed, octaves, lacunarity, scale]
            c = db.cursor()
            c.execute(f"UPDATE Maps SET MapArr = ? WHERE id = ?", (str(nums), id_map))
            db.commit()
            db.close()
            f = open(f"MapsFolder/Map{id}.txt", "w")
            f.write(str(nums))
            f.close()
        self.open_back_window()

    def open_back_window(self):
        self.back_window = InGameWindow_created()
        self.back_window.show()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
