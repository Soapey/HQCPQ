from PyQt5.QtWidgets import QApplication
from .gui.classes.WindowState import WindowState
from .gui.classes.MainWindow import MainWindow 
from .db.config import start
from .db import SQLCursor
import sys


def main():

    SQLCursor.build_name = 'test'

    start(SQLCursor.build_name)

    app = QApplication(sys.argv)

    main = MainWindow(0, 0, 300, 200, WindowState.MAXIMISED, 'HQCPQ')

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()