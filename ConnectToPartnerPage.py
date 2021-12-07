from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt
from MessageWindows import ErrorMessageWindow
from functools import partial
from Coders import jsonToBytes, intToBytes, bytesToJson
from secret_list_creator import create_points_list, point_list_to_dictionary, point_list_from_dictionary\
, compute_common_point_list, compute_index_lists_for_free_slots
import random
import tinyec.registry as reg

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
            LocalMeetings = [meeting.getDateAndTime() for meeting in localMeetingList]  # These are the meetings to send, please change this to the DH encryption.
            private_input = random.randint(1, 100)
            LocalMeetingsPoints, LocalMeetingsTuples = create_points_list(LocalMeetings, 15, private_input)

            client.sendData(jsonToBytes(point_list_to_dictionary(LocalMeetingsPoints)))
            MeetingsPointsFromMySlots = point_list_from_dictionary(bytesToJson(client.receiveData()))  # These are B's meetings they need to be DH encrypted with A's key.
            CommonMeetingsPointsFromOtherParty = point_list_from_dictionary(bytesToJson(client.receiveData()))
            CommonMeetingsPointsFromMySlots = compute_common_point_list(MeetingsPointsFromMySlots, private_input)
            # compare encryptedMeetingsFromB and encryptedLocalMeetingsFromB
            MyIndexList, OtherPartyIndexList = compute_index_lists_for_free_slots(CommonMeetingsPointsFromMySlots
                                                                                  , CommonMeetingsPointsFromOtherParty)
            CommonMeetingIndex = random.randint(0, len(MyIndexList) - 1)
            if len(MyIndexList) == 0:
                pass # should close connection if there no meeting
            else:
                client.sendData(intToBytes(OtherPartyIndexList[CommonMeetingIndex]))
                client.sendData(jsonToBytes({
                'title': localMeetingList[CommonMeetingIndex].title,
                'description': localMeetingList[CommonMeetingIndex].description
            }))
            client.bye()
        except Exception as exc:
            errorWindow = ErrorMessageWindow('Connection lost', str(exc))
            #errorWindow = ErrorMessageWindow('Connection lost', 'Error occurred while communicating with partner.')
            errorWindow.exec_()
