from PyQt5.QtWidgets import QMessageBox


class InfoMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.exec()
