from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt
from MessageWindows import ErrorMessageWindow
from functools import partial
from Coders import jsonToBytes, intToBytes, bytesToJson
from secret_list_creator import create_points_list, point_list_to_dictionary, point_list_from_dictionary\
, compute_common_point_list, compute_index_lists_for_free_slots, get_noise_meetings_indices
import random


class ConnectToPartnerPage(QMainWindow):
    def __init__(self, networkInterface, meetingHandler):
        super().__init__()
        self.networkInterface = networkInterface
        self.meetingHandler = meetingHandler
        self.selectedMeeting = None
        self.title = 'Connect to partner'
        self.width = 520
        self.height = 410
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

        label = QLabel(self.centralwidget)
        label.setGeometry(10, 90, 150, 30)
        label.setText('Meeting title:')

        title = QLineEdit(self.centralwidget)
        title.setGeometry(160, 90, 200, 30)
        title.setText('alma')

        label = QLabel(self.centralwidget)
        label.setGeometry(10, 130, 150, 30)
        label.setText('Meeting description:')

        description = QTextEdit(self.centralwidget)
        description.setStyleSheet("font-size:15px;padding:2px;")
        description.setGeometry(10, 170, 500, 70)
        description.setText('barack')

        logLabel = QTextEdit(self.centralwidget)
        logLabel.setReadOnly(True)
        logLabel.setStyleSheet("background-color:transparent;font-size:10px;padding:2px;border-radius:2px;")
        logLabel.setGeometry(10, 250, 500, 150)

        connection = QPushButton(self.centralwidget)
        connection.setGeometry(370, 130, 140, 30)
        connection.setText('Connect')
        connection.clicked.connect(partial(self.connectionClicked, ip, port, title, description, logLabel))

        self.show()

    def connectionClicked(self, ip, port, title, description, log):
        client = None
        try:
            client = self.networkInterface.createClient(ip.text(), int(port.text()))
            log.append('Connected to the partner.')
            weeks = self.meetingHandler.getMeetingWeeks(self.meetingHandler.meetings)
            meetingLength = self.meetingHandler.getAndCeheckTheLengthOfTheMeetings(self.meetingHandler.meetings)
            noiseMeetingsDict = self.meetingHandler.createNoiseMeeitngs(weeks, meetingLength)
            log.append('Noise is added to the meetings.')
            client.sendData(jsonToBytes({
                'weeks': weeks,
                'meetingLength': meetingLength
            }))
            log.append('Basic time information sent to the partner.')
            #self.meetingHandler.appendMeetings(noiseMeetingsDict)
            noiseMeetingsList = self.meetingHandler.meetingsToList(noiseMeetingsDict)
            localMeetingList = self.meetingHandler.meetingsToList(self.meetingHandler.meetings)
            localMeetings = [meeting.getDateAndTime() for meeting in localMeetingList]
            noiseMeetings = [meeting.getDateAndTime() for meeting in noiseMeetingsList]
            noiseMeetingsIndices = get_noise_meetings_indices(localMeetings, noiseMeetings)
            private_input = random.randint(1, 100)
            localMeetingsPoints, localMeetingsTuples = create_points_list(localMeetings, private_input)
            log.append('Meetings are encrypted.')
            client.sendData(jsonToBytes(point_list_to_dictionary(localMeetingsPoints)))
            log.append('Meetings sent to the partner')
            meetingsPointsFromOtherParty = point_list_from_dictionary(bytesToJson(client.receiveData()))
            log.append('Own meetings encrypted by partner too are received.')
            commonMeetingsPointsFromMySlots = point_list_from_dictionary(bytesToJson(client.receiveData()))
            log.append('Partner\'s meetings are received')
            commonMeetingsPointsFromOtherParty = compute_common_point_list(meetingsPointsFromOtherParty, private_input)
            myIndexList, otherPartyIndexList = compute_index_lists_for_free_slots(commonMeetingsPointsFromOtherParty, commonMeetingsPointsFromMySlots)
            if len(myIndexList) == 0:
                log.append('No common meeting')
                client.bye()
            else:
                for noise_index in noiseMeetingsIndices:
                    if noise_index in myIndexList:
                        index_of_noise_index = myIndexList.index(noise_index)
                        del myIndexList[index_of_noise_index]
                        del otherPartyIndexList[index_of_noise_index]
                if len(myIndexList) == 0:
                    log.append('No common meeting')
                    client.bye()
                elementOfIndexList = random.randint(0, len(myIndexList) - 1)
                otherPartyIndex = otherPartyIndexList[elementOfIndexList]
                myIndex = myIndexList[elementOfIndexList]
                log.append('Common meeting found.')
                client.sendData(intToBytes(otherPartyIndex))
                client.sendData(jsonToBytes({
                    'title': title.text(),
                    'description': description.toPlainText()
                }))
                log.append('Meeting title and description sent.')
                client.bye()
                log.append('Connection closed.')
                self.selectedMeeting = localMeetingList[myIndex]
                self.selectedMeeting.title = title.text()
                self.selectedMeeting.description = description.toPlainText()
                log.append('Selected meeting will be added to the meetings after this window is closed.')
                self.close()
        except Exception as exc:
            if client:
                client.bye()
            #errorWindow = ErrorMessageWindow('Connection lost', str(exc))
            errorWindow = ErrorMessageWindow('Connection lost', 'Error occurred while communicating with partner.')
            errorWindow.exec_()
