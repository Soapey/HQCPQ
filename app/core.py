from PyQt5.QtWidgets import QApplication
from .gui.classes.WindowState import WindowState
from .gui.classes.MainWindow import MainWindow 
from .db.config import start
from .db import SQLCursor
import sys


def test():

    from app.classes.Quote import Quote
    from app.classes.QuoteItem import QuoteItem
    from datetime import datetime

    SQLCursor.build_name = 'production'
    
    start(SQLCursor.build_name, True)

    q = Quote(None, datetime.today(), datetime.today(), 'Grant Soper', '4 Bilmark Drive', 'Raymond Terrace', '0481552395')
    q.insert()

    i1 = QuoteItem(None, q.id, 'Truck', 12.5, 10, 'CMS', 14)
    i1.insert()

    i2 = QuoteItem(None, q.id, 'Trailer', 20, 10, '40mm Scalps', 10)
    i2.insert()

    print(len(QuoteItem.get()))

    q.delete()

    print(len(QuoteItem.get()))

def main():

    SQLCursor.build_name = 'production'

    start(SQLCursor.build_name)

    app = QApplication(sys.argv)

    main = MainWindow(0, 0, 300, 200, WindowState.MAXIMISED, 'HQCPQ')

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()