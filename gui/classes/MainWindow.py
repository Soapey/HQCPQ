from PyQt5.QtWidgets import QMainWindow
from .WinState import WinState


class MainWindow():

    def __init__(self, xpos: int, ypos: int, width: int, height: int, _state: WinState, title: str = 'Main Window') -> None:

        self.frame = QMainWindow()
        self.frame.setGeometry(xpos, ypos, width, height)
        self.frame.setWindowTitle(title)
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):

        self._state = val

        match val:
            case WinState.MINIMISED:
                self.frame.showMinimized()
            case WinState.NORMAL:
                self.frame.show()
            case WinState.MAXIMISED:
                self.frame.showMaximized()