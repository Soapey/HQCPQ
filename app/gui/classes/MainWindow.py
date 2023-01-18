from PyQt5.QtWidgets import QMainWindow
from .WindowState import WindowState


class MainWindow(QMainWindow):

    def __init__(self, xpos: int, ypos: int, width: int, height: int, _state: WindowState, title: str = 'Main Window') -> None:
        super().__init__()
        
        self.setGeometry(xpos, ypos, width, height)
        self.setWindowTitle(title)
        self.state = _state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):

        self._state = val

        match val:
            case WindowState.MINIMISED:
                self.showMinimized()
            case WindowState.NORMAL:
                self.show()
            case WindowState.MAXIMISED:
                self.showMaximized()