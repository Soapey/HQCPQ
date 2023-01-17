from PyQt5.QtWidgets import QMainWindow
from WinState import WinState


class MainWindow():

    def __init__(self, xpos: int, ypos: int, width: int, height: int, _state: WinState, title: str = 'Main Window') -> None:

        self.frame = QMainWindow()
        self.frame.setGeometry(xpos, ypos, width, height)
        self.frame.setWindowTitle(title)
        self._state = self.state(_state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, _state) -> WinState:

        self._state = _state

        match _state:
            case WinState.MINIMISED:
                self.frame.showMinimized()
            case WinState.NORMAL:
                self.frame.show()
            case WinState.MAXIMISED:
                self.frame.showMaximized()