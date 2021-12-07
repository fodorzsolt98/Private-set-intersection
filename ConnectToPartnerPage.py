from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt
from MessageWindows import ErrorMessageWindow
from functools import partial
from Coders import jsonToBytes, intToBytes, bytesToJson


class ConnectToPartnerPage(QMainWindow):
    def __init__(self, networkInterface, meetingHandler):
        super().__init__()
        self.networkInterface = networkInterface
        self.meetingHandler = meetingHandler
        self.title = 'Connect to partner'
        self.width = 520
        self.height = 250
        self.initWindow()


    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowModality(Qt.ApplicationModal)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)
        self.initUI()

    def initUI(self):
        label = QLabel(self.centralwidget)
        label.setGeometry(10, 10, 150, 30)
        label.setText('IPv4 address of the partner:')

        ip = QLineEdit(self.centralwidget)
        ip.setGeometry(160, 10, 200, 30)
        ip.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"), self))
        ip.setText('127.0.0.1')

        label = QLabel(self.centralwidget)
        label.setGeometry(10, 50, 150, 30)
        label.setText('Port number of the partner:')

        port = QLineEdit(self.centralwidget)
        port.setGeometry(160, 50, 200, 30)
        port.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{1,5}"), self))
        port.setText('5555')

        connection = QPushButton(self.centralwidget)
        connection.setGeometry(370, 50, 140, 30)
        connection.setText('Connect')
        connection.clicked.connect(partial(self.connectionClicked, ip.text(), int(port.text())))

        descriptionLabel = QTextEdit(self.centralwidget)
        descriptionLabel.setReadOnly(True)
        #descriptionLabel.setStyleSheet("background-color:transparent;font-size:15px;padding:2px;border-radius:2px;")
        descriptionLabel.setGeometry(10, 90, 500, 150)
        descriptionLabel.setText('')

        self.show()

    def connectionClicked(self, ip, port):
        try:
            client = self.networkInterface.createClient(ip, port)
            weeks = self.meetingHandler.getMeetingWeeks(self.meetingHandler.meetings)
            meetingLength = self.meetingHandler.getAndCeheckTheLengthOfTheMeetings(self.meetingHandler.meetings)
            self.meetingHandler.createNoiseMeeitngs(weeks, meetingLength)
            client.sendData(jsonToBytes({
                'weeks': weeks,
                'meetingLength': meetingLength
            }))
            self.meetingHandler.appendMeetings(self.meetingHandler.createNoiseMeeitngs(weeks, meetingLength))
            localMeetingList = self.meetingHandler.meetingsToList(self.meetingHandler.meetings)
            encryptedLocalMeetings = [meeting.getDateAndTime() for meeting in localMeetingList]  # These are the meetings to send, please change this to the DH encryption.
            client.sendData(jsonToBytes(encryptedLocalMeetings))
            encryptedMeetingsFromB = bytesToJson(client.receiveData())  # These are B's meetings they need to be DH encrypted with A's key.
            encryptedLocalMeetingsFromB = bytesToJson(client.receiveData())
            # compare encryptedMeetingsFromB and encryptedLocalMeetingsFromB
            client.sendData(intToBytes(0))  # should close connection if there no meeting
            client.sendData(jsonToBytes({
                'title': 'alma',
                'description': 'barack'
            }))
            client.bye()
        except Exception as exc:
            errorWindow = ErrorMessageWindow('Connection lost', str(exc))
            #errorWindow = ErrorMessageWindow('Connection lost', 'Error occurred while communicating with partner.')
            errorWindow.exec_()
