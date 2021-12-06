from PyQt5.QtWidgets import QMessageBox


Ok = QMessageBox.Ok
Cancel = QMessageBox.Cancel


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


class WarningMessageWindowWithButtons(QMessageBox):
    def __init__(self, text, description, buttons):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Warning")
        self.setText(text)
        self.setInformativeText(description)
        self.setStandardButtons(buttons)


class InformationMessageWindowWithButtons(QMessageBox):
    def __init__(self, text, description, buttons):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("Information")
        self.setText(text)
        self.setInformativeText(description)
        self.setStandardButtons(buttons)
