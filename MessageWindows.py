from PyQt5.QtWidgets import QMessageBox


class ErrorMessageWindow(QMessageBox):
    def __init__(self, text, description):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error")
        self.setText(text)
        self.setInformativeText(description)


class WarningMessageWindow(QMessageBox):
    def __init__(self, text, description):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Warning")
        self.setText(text)
        self.setInformativeText(description)
