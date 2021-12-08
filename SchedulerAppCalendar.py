from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMenu, QMenuBar
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QEventLoop, pyqtSlot
from datetime import date, timedelta
from Meeting import Meeting
from MeetingInfoPage import MeetingInfoPage
from AddNewMeetingPage import AddNewMeetingPage
from ConnectToPartnerPage import ConnectToPartnerPage
from NetworkInterface import NetworkInterface
from MessageWindows import WarningMessageWindow
from MeetingHandler import MeetingHandler
import sys


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
        self.meetingHandler = MeetingHandler()
        self.meetingLabels = []
        self.networkInterface = NetworkInterface(self.meetingHandler, self, 5555)
        self.networkInterface.startServer()
        self.reloadListeners = []
        #Remove dummy meetings in release
        self.meetingHandler.appendMeetings(self.meetingHandler.createDummyMeetings(10, date.today() - timedelta(days=3),  date.today() - timedelta(days=10)))
        #--------------------------------
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)
        self.initMenu()
        self.initTableGUI()
        self.show()

    def closeEvent(self, e):
        window = WarningMessageWindow('Application is closing', 'The application is closing, the server will stop and the client services will be aborted.')
        #window.exec_()
        self.networkInterface.stopServer()

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
        addNew.mouseReleaseEvent = self.addNewMeetingClicked
        #test = QMenu('&test connetcion', self)
        #test.mouseReleaseEvent = self.testConnection
        self.menuBar.addMenu(addNew)
        #self.menuBar.addMenu(test)

    def testConnection(self, e):
        meetingHandler = MeetingHandler()
        meetingHandler.appendMeetings(self.meetingHandler.createMeetingSequences(date.today(), 480, 600, 60))
        self.connectToPartener(meetingHandler)

    def addNewMeetingClicked(self, e):
        newMeetingPage = AddNewMeetingPage(self.meetingHandler.meetings)
        newMeetingPage.show()
        loop = QEventLoop()
        newMeetingPage.closeEvent = lambda e: loop.quit()
        loop.exec()
        if newMeetingPage.connectToPartner and (len(newMeetingPage.meetingHandler.meetings.keys()) > 0):
            self.connectToPartener(newMeetingPage.meetingHandler)

    def connectToPartener(self, meetings):
        connectionPage = ConnectToPartnerPage(self.networkInterface, meetings)
        connectionPage.show()
        loop = QEventLoop()
        connectionPage.closeEvent = lambda e: loop.quit()
        loop.exec()
        if connectionPage.selectedMeeting:
            self.meetingHandler.addMeeting(connectionPage.selectedMeeting)
            self.loadMeetings()

    def initTableGUI(self):
        daysList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(0, len(daysList)):
            label = QLabel(self.centralwidget)
            label.setGeometry(self.tableLeft + 30 + i * 100, self.tableTop - 50, 100, 20)
            label.setText(daysList[i])

        today = date.today()
        weekDay = today.weekday()
        for i in range(0, 7):
            label = QLabel(self.centralwidget)
            label.setGeometry(self.tableLeft + 20 + i * 100, self.tableTop - 25, 100, 20)
            label.setText((today + timedelta(days=(i - weekDay))).strftime("%Y-%m-%d"))
            self.dateLables.append(label)

        for i in range(0, 10):
            label = QLabel(self.centralwidget)
            label.setGeometry(self.tableLeft - 40, self.tableTop + i * 24, 40, 24)
            label.setText(f'0{i}:00')
        for i in range(10, 24):
            label = QLabel(self.centralwidget)
            label.setGeometry(self.tableLeft - 40, self.tableTop + i * 24, 40, 24)
            label.setText(f'{i}:00')

        self.loadMeetings()

        previousWeekButton = QPushButton(self.centralwidget)
        previousWeekButton.setGeometry(5, self.tableTop - 20, 40, 20)
        previousWeekButton.setText('<')
        previousWeekButton.clicked.connect(self.previousWeekButtonClicked)

        nextWeekButton = QPushButton(self.centralwidget)
        nextWeekButton.setGeometry(self.tableLeft + 705, self.tableTop - 20, 40, 20)
        nextWeekButton.setText('>')
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

    @pyqtSlot()
    def loadMeetings(self):
        for label in self.meetingLabels:
            label.deleteLater()
        self.meetingLabels = []

        y = self.currentWeekStart.year
        w = self.currentWeekStart.isocalendar().week
        if (y in self.meetingHandler.meetings) and (w in self.meetingHandler.meetings[y]):
            for meeting in self.meetingHandler.meetings[y][w]:
                label = QLabel(self.centralwidget)
                label.setGeometry(self.tableLeft + meeting.startDate.weekday() * 100 + 2, self.tableTop + int(meeting.startTime / 2.5), 96, int(meeting.length / 2.5))
                label.setText(meeting.title)
                label.setStyleSheet("background-color:#315dd6;padding:2px;border-radius:2px;")
                label.meeting = meeting
                label.mouseDoubleClickEvent = self.meetingLabelDoubleClicked
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
