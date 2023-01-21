from PyQt5.QtWidgets import QApplication, QMainWindow
from .db.config import start
from .db import SQLCursor
from .gui.components.main import Ui_MainWindow
import sys



def main():

    SQLCursor.build_name = 'production'

    start(SQLCursor.build_name)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()