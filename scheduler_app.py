from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QWidget, QComboBox, QTextEdit
from functools import partial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMenu, QMenuBar
from PyQt5.QtGui import QPainter, QPen, QRegularExpressionValidator
from PyQt5.QtCore import Qt, QEventLoop, QRegularExpression
from datetime import date, timedelta
from random import randint, choice
from Meeting import Meeting
from MeetingInfoPage import MeetingInfoPage
import sys
import string

class SchedulerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title='Reserve new meeting'
        self.width = 720
        self.height = 330
        self.dateLables = []
        self.currentWeekStart = date.today() - timedelta(days=(date.today().weekday()))
        self.meetings = []
        self.initWindow()
        self.initUI()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)

    def initUI(self):

        days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        label = QLabel(self.centralwidget)
        label.setGeometry(155, 10, 50, 30)
        label.setText('From')

        label = QLabel(self.centralwidget)
        label.setGeometry(280, 10, 50, 30)
        label.setText('To')

        label = QLabel(self.centralwidget)
        label.setGeometry(500, 10, 100, 30)
        label.setText('Registered meetings')

        registeredMeetingLabel = QTextEdit(self.centralwidget)
        registeredMeetingLabel.setReadOnly(True)
        registeredMeetingLabel.setStyleSheet("background-color:transparent;font-size:15px;padding:2px;border-radius:2px;")
        registeredMeetingLabel.setGeometry(460, 50, 250, 230)

        today = date.today()
        weekDay = today.weekday()

        previousWeekButton = QPushButton(self.centralwidget)
        previousWeekButton.setGeometry(10, 10, 40, 20)
        previousWeekButton.setText('<')
        previousWeekButton.clicked.connect(self.previousWeekButtonClicked)

        nextWeekButton = QPushButton(self.centralwidget)
        nextWeekButton.setGeometry(50, 10, 40, 20)
        nextWeekButton.setText('>')
        nextWeekButton.clicked.connect(self.nextWeekButtonClicked)

        checkTimeWithPartner = QPushButton(self.centralwidget)
        checkTimeWithPartner.setGeometry(500, 290, 150, 30)
        checkTimeWithPartner.setText('Check with partner')
        checkTimeWithPartner.clicked.connect(self.previousWeekButtonClicked)

        for i in range(0, len(days_list)):

            label = QLabel(self.centralwidget)
            label.setGeometry(10, 50 + i * 40, 100, 20)
            label.setText(days_list[i])

            label = QLabel(self.centralwidget)
            label.setGeometry(10, 65 + i * 40, 100, 20)
            label.setText((today + timedelta(days=(i - weekDay))).strftime("%Y-%m-%d"))
            self.dateLables.append(label)

            startHour, startMinute = self.createTimeInputGUI(110, i)
            endHour, endMinute = self.createTimeInputGUI(230, i)

            addButton = QPushButton(self.centralwidget)
            addButton.setGeometry(350, 50 + i * 40, 100, 30)
            addButton.setText('Add')

            addButton.clicked.connect(partial(self.registrationClicked
                                               , startHour
                                               , startMinute
                                               , endHour
                                               , endMinute
                                               , i
                                               , registeredMeetingLabel))

    def registrationClicked(self, startHour, startMinute, endHour, endMinute, daydiff, label):
        if startHour.text() and endHour.text():
            startTime = int(startHour.text()) * 60 + int(startMinute.currentText())
            endTime = int(endHour.text()) * 60 + int(endMinute.currentText())
            meeting = Meeting(self.currentWeekStart + timedelta(days=daydiff), startTime, endTime - startTime)
            self.meetings.append(meeting)
            label.append(meeting.getDateAndTime())

    def createTimeInputGUI(self, left, iteration):
        hour = QLineEdit(self.centralwidget)
        hour.setGeometry(left, 50 + iteration * 40, 50, 30)
        hour.setValidator(QRegularExpressionValidator(QRegularExpression("(2[0-3]|1[0-9]|[0-9])"), self))

        label = QLabel(self.centralwidget)
        label.setGeometry(left + 55, 50 + iteration * 40, 5, 30)
        label.setText(':')

        minute = QComboBox(self.centralwidget)
        minute.setGeometry(left + 60, 50 + iteration * 40, 50, 30)
        minute.addItems(['00', '15', '30', '45'])
        return hour, minute

    def dateRefresh(self, direction):
        self.currentWeekStart = self.currentWeekStart + timedelta(days=(direction * 7))
        for i in range(0, 7):
            self.dateLables[i].setText((self.currentWeekStart + timedelta(days=i)).strftime("%Y-%m-%d"))

    def previousWeekButtonClicked(self):
        self.dateRefresh(-1)

    def nextWeekButtonClicked(self):
        self.dateRefresh(1)


def run_app():
    app = QApplication(sys.argv)
    window = SchedulerWindow()
    window.show()
    sys.exit(app.exec_())

run_app()

