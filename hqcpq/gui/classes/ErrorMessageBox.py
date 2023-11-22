from PyQt5.QtWidgets import QMessageBox


class ErrorMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.exec()
