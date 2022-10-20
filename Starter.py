import sys
from PyQt5.QtWidgets import *
import main


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    Window = main.MainWindow()
    Window.show()
    sys.exit(app.exec_())

