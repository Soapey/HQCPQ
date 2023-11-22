from PyQt5.QtWidgets import QMessageBox


class AskYesNoMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Question)
        self.setText(self.message)
        self.addButton(QMessageBox.StandardButton.Yes, "Yes")
        self.addButton(QMessageBox.StandardButton.No, "No")
        result = self.exec()

        if result == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False
