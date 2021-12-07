from functools import partial
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt
from datetime import date, timedelta
from Meeting import Meeting
from MeetingHandler import MeetingHandler
from MessageWindows import WarningMessageWindowWithButtons, WarningMessageWindow

class AddNewMeetingPage(QMainWindow):
    def __init__(self, existingMeetings):
        super().__init__()
        self.title='Reserve new meeting'
        self.width = 720
        self.height = 330
        self.dateLables = []
        self.currentWeekStart = date.today() - timedelta(days=(date.today().weekday()))
        self.meetingHandler = MeetingHandler()
        self.existingMeetings = existingMeetings
        self.connectToPartner = False
        self.initWindow()
        self.initUI()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowModality(Qt.ApplicationModal)
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
        label.setGeometry(470, 250, 50, 30)
        label.setText('Length:')

        label = QLabel(self.centralwidget)
        label.setGeometry(540, 10, 100, 30)
        label.setText('Registered time slots')

        registeredMeetingLabel = QTextEdit(self.centralwidget)
        registeredMeetingLabel.setReadOnly(True)
        #registeredMeetingLabel.setStyleSheet("background-color:transparent;font-size:15px;padding:2px;border-radius:2px;")
        registeredMeetingLabel.setGeometry(460, 50, 250, 190)

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
        checkTimeWithPartner.clicked.connect(self.checkMeetingWithPartner)

        lengthHour, lengthMinute = self.createTimeInputGUI(510, 5)

        resetLengthButton = QPushButton(self.centralwidget)
        resetLengthButton.setGeometry(630, 250, 80, 30)
        resetLengthButton.setText('Reset length')
        resetLengthButton.clicked.connect(partial(self.resetLengthClicked, registeredMeetingLabel, lengthHour, lengthMinute))

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
                                               , lengthHour
                                               , lengthMinute
                                               , i
                                               , registeredMeetingLabel))

    def registrationClicked(self, startHour, startMinute, endHour, endMinute, lengthHour, lengthMinute, daydiff, label):
        if not lengthHour.text() and (lengthMinute.currentText() == '00'):
            message = WarningMessageWindow('No predefined length.', 'Before save time slot, the length of the time slots must be set.')
            message.exec_()
        elif startHour.text() and endHour.text():
            startTime = int(startHour.text()) * 60 + int(startMinute.currentText())
            lengthTime = (0 if lengthHour.text() == '' else int(lengthHour.text()) * 60) + int(lengthMinute.currentText())
            endTime = int(endHour.text()) * 60 + int(endMinute.currentText())

            day = self.currentWeekStart + timedelta(days=daydiff)
            meetings = self.meetingHandler.createMeetingSequences(day, startTime, endTime, lengthTime)
            meetings = self.meetingHandler.filterCollosions(self.existingMeetings, meetings)
            meetings = self.meetingHandler.filterCollosions(self.meetingHandler.meetings, meetings)
            self.meetingHandler.appendMeetings(meetings)

            for meeting in meetings[day.year][day.isocalendar().week]:
                label.append(meeting.getDateAndTime())
            lengthHour.setEnabled(False)
            lengthMinute.setEnabled(False)
        else:
            message = WarningMessageWindow('Not valid interval.', 'Time slot has no start or ending time.')
            message.exec_()

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

    def resetLengthClicked(self, registeredMeetingLabel, lengthHour, lengthMinute):
        message = WarningMessageWindowWithButtons(text='Reset meeting length'
                                                  , description='If you reset the length of the meetings, the newly added time slots will be lost.'
                                                  , buttons=QMessageBox.Cancel | QMessageBox.Ok)
        if message.exec_() == QMessageBox.Ok:
            self.meetingHandler.meetings = {}
            registeredMeetingLabel.setText('')
            lengthHour.setEnabled(True)
            lengthMinute.setEnabled(True)

    def checkMeetingWithPartner(self):
        self.connectToPartner = True
        self.close()

    def dateRefresh(self, direction):
        self.currentWeekStart = self.currentWeekStart + timedelta(days=(direction * 7))
        for i in range(0, 7):
            self.dateLables[i].setText((self.currentWeekStart + timedelta(days=i)).strftime("%Y-%m-%d"))

    def previousWeekButtonClicked(self):
        self.dateRefresh(-1)

    def nextWeekButtonClicked(self):
        self.dateRefresh(1)
