from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMenu, QMenuBar
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QEventLoop
from datetime import date, timedelta
from random import randint, choice
from Meeting import Meeting
from MeetingInfoPage import MeetingInfoPage
import sys
import string


class SchedulerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Privacy preserving scheduling app'
        self.width = 800
        self.height = 670
        self.tableTop = 80
        self.tableLeft = 50
        self.dateLables = []
        self.currentWeekStart = date.today() - timedelta(days=(date.today().weekday()))
        self.meetings = {}
        self.meetingLabels = []
        #Remove dummy meetings in release
        self.dummyMeetings(10, date.today() - timedelta(days=3),  date.today() - timedelta(days=10))
        #--------------------------------
        self.initWindow()


    def dummyMeetings(self, count, start, end):
        dateDiff = abs((end - start).days)
        for i in range(0, count):
            rdate = start + timedelta(days=randint(0, dateDiff))
            y = rdate.year
            w = rdate.isocalendar().week
            if y not in self.meetings:
                self.meetings[y] = {}
            if w not in self.meetings[y]:
                self.meetings[y][w] = []
            self.meetings[y][w].append(Meeting(
                startDate=rdate,
                startTime=randint(50, 260) *5,
                length=randint(6, 24) * 5,
                title=''.join(choice(string.ascii_lowercase) for i in range(randint(5, 20))),
                description=''.join(choice(string.ascii_lowercase) for i in range(randint(20, 100)))))


    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)
        self.initMenu()
        self.initTableGUI()
        self.show()


    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        for i in range(1, 7):
            x = self.tableLeft + i * 100
            painter.drawLine(x, self.tableTop, x, self.tableTop + 576)
        for i in range(1, 24):
            y = self.tableTop + i * 24
            painter.drawLine(self.tableLeft, y, self.tableLeft + 700, y)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawRect(self.tableLeft, self.tableTop, 700, 576)


    def initMenu(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        addNew = QMenu('&Add new', self)
        self.menuBar.addMenu(addNew)


    def initTableGUI(self):
        daysList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(0, len(daysList)):
            label = QLabel()
            label.setGeometry(self.tableLeft + 30 + i * 100, self.tableTop - 50, 100, 20)
            label.setText(daysList[i])
            label.setParent(self.centralwidget)

        today = date.today()
        weekDay = today.weekday()
        for i in range(0, 7):
            label = QLabel()
            label.setGeometry(self.tableLeft + 20 + i * 100, self.tableTop - 25, 100, 20)
            label.setText((today + timedelta(days=(i - weekDay))).strftime("%Y-%m-%d"))
            label.setParent(self.centralwidget)
            self.dateLables.append(label)

        for i in range(0, 10):
            label = QLabel()
            label.setGeometry(self.tableLeft - 40, self.tableTop + i * 24, 40, 24)
            label.setText(f'0{i}:00')
            label.setParent(self.centralwidget)
        for i in range(10, 24):
            label = QLabel()
            label.setGeometry(self.tableLeft - 40, self.tableTop + i * 24, 40, 24)
            label.setText(f'{i}:00')
            label.setParent(self.centralwidget)

        self.loadMeetings()

        previousWeekButton = QPushButton()
        previousWeekButton.setGeometry(5, self.tableTop - 20, 40, 20)
        previousWeekButton.setText('<')
        previousWeekButton.setParent(self.centralwidget)
        previousWeekButton.clicked.connect(self.previousWeekButtonClicked)

        nextWeekButton = QPushButton()
        nextWeekButton.setGeometry(self.tableLeft + 705, self.tableTop - 20, 40, 20)
        nextWeekButton.setText('>')
        nextWeekButton.setParent(self.centralwidget)
        nextWeekButton.clicked.connect(self.nextWeekButtonClicked)


    def dateRefresh(self, direction):
        self.currentWeekStart = self.currentWeekStart + timedelta(days=(direction * 7))
        for i in range(0, 7):
            self.dateLables[i].setText((self.currentWeekStart + timedelta(days=i)).strftime("%Y-%m-%d"))
        self.loadMeetings()


    def previousWeekButtonClicked(self):
        self.dateRefresh(-1)


    def nextWeekButtonClicked(self):
        self.dateRefresh(1)


    def loadMeetings(self):
        for label in self.meetingLabels:
            label.deleteLater()
        self.meetingLabels = []

        y = self.currentWeekStart.year
        w = self.currentWeekStart.isocalendar().week
        if (y in self.meetings) and (w in self.meetings[y]):
            for meeting in self.meetings[y][w]:
                label = QLabel()
                label.setGeometry(self.tableLeft + meeting.startDate.weekday() * 100 + 2, self.tableTop + int(meeting.startTime / 2.5), 96, int(meeting.length / 2.5))
                label.setText(meeting.title)
                label.setStyleSheet("background-color:#315dd6;padding:2px;border-radius:2px;")
                label.meeting = meeting
                label.mouseDoubleClickEvent = self.meetingLabelDoubleClicked
                label.setParent(self.centralwidget)
                label.show()
                self.meetingLabels.append(label)

    def getMeetingLabelByPos(self, pos):
        for label in self.meetingLabels:
            if ((label.x() < pos.x()) and (label.x() + label.width() > pos.x())) and ((label.y() < pos.y()) and (label.y() + label.height() > pos.y())):
                return label
        return None

    def meetingLabelDoubleClicked(self, e):
        meetingLabel = self.getMeetingLabelByPos(e.windowPos())
        if meetingLabel:
            infoPage = MeetingInfoPage(meetingLabel.meeting)
            infoPage.show()
            loop = QEventLoop()
            infoPage.closeEvent = lambda e: loop.quit()
            loop.exec()


def runApp():
    app = QApplication(sys.argv)
    window = SchedulerWindow()
    sys.exit(app.exec_())


runApp()
