from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTextEdit
from PyQt5.QtCore import Qt

class MeetingInfoPage(QMainWindow):
    def __init__(self, meeting):
        super().__init__()
        self.meeting = meeting
        self.title = meeting.title
        self.width = 520
        self.height = 270
        self.initWindow()


    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowModality(Qt.ApplicationModal)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)

        titleLabel = QLabel(self.centralwidget)
        titleLabel.setGeometry(10, 10, 500, 50)
        titleLabel.setText(self.meeting.title)
        titleLabel.setStyleSheet("font-size:40px")

        titleLabel = QLabel(self.centralwidget)
        titleLabel.setGeometry(10, 60, 500, 50)
        titleLabel.setText(f'In {self.meeting.startDate} from {self.meeting.getStartTime()} to {self.meeting.getEndTime()}')
        titleLabel.setStyleSheet("font-size:20px")

        descriptionLabel = QTextEdit(self.centralwidget)
        descriptionLabel.setReadOnly(True)
        descriptionLabel.setStyleSheet("background-color:transparent;font-size:15px;padding:2px;border-radius:2px;")
        descriptionLabel.setGeometry(10, 110, 500, 150)
        descriptionLabel.setText(self.meeting.description)

        self.show()
