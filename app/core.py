from PyQt5.QtWidgets import QApplication
from .gui.classes.WindowState import WindowState
from .gui.classes.MainWindow import MainWindow 
import sys


build_name = sys.argv[1]


def main():

    app = QApplication(sys.argv)

    main = MainWindow(0, 0, 300, 200, WindowState.MAXIMISED, 'HQCPQ')

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()