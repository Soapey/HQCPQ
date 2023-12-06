from PyQt5.QtWidgets import QMessageBox


class AskYesNoMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.state = False
        self.setIcon(QMessageBox.Question)
        self.setText(self.message)
        self.addButton(QMessageBox.StandardButton.Yes)
        self.addButton(QMessageBox.StandardButton.No)
        result = self.exec()
        self.state = result == QMessageBox.StandardButton.Yes
