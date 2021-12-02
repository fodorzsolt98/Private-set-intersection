from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt
from MessageWindows import ErrorMessageWindow
from functools import partial
import socket


class ConnectToPartnerPage(QMainWindow):
    def __init__(self, networkInterface, meetings):
        super().__init__()
        self.networkInterface = networkInterface
        self.meetings = meetings
        self.title = 'Connect to partner'
        self.width = 520
        self.height = 270
        self.initWindow()


    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowModality(Qt.ApplicationModal)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 0, self.width, self.height)
        self.initUI()

    def initUI(self):
        label = QLabel()
        label.setGeometry(10, 10, 150, 30)
        label.setText('IPv4 address of the partner:')
        label.setParent(self.centralwidget)

        ip = QLineEdit(self.centralwidget)
        ip.setGeometry(160, 10, 200, 30)
        ip.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"), self))
        ip.setText('127.0.0.1')

        label = QLabel()
        label.setGeometry(10, 50, 150, 30)
        label.setText('Port number of the partner:')
        label.setParent(self.centralwidget)

        port = QLineEdit(self.centralwidget)
        port.setGeometry(160, 50, 200, 30)
        port.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{1,5}"), self))
        port.setText('5555')

        connectionTest = QPushButton(self.centralwidget)
        connectionTest.setGeometry(370, 50, 100, 30)
        connectionTest.setText('Test connection')
        connectionTest.clicked.connect(partial(self.testConnectionClicked, ip.text(), int(port.text())))

        descriptionLabel = QTextEdit(self.centralwidget)
        descriptionLabel.setReadOnly(True)
        #descriptionLabel.setStyleSheet("background-color:transparent;font-size:15px;padding:2px;border-radius:2px;")
        descriptionLabel.setGeometry(10, 110, 500, 150)
        descriptionLabel.setText('')

        self.show()

    def testConnectionClicked(self, ip, port):
        try:
            conn = self.networkInterface.socketInit()
            conn.connect((ip, port))
            conn.send('hello'.encode('utf-8'))
            conn.close()
        except:
            errorWindow = ErrorMessageWindow('Connection lost', 'Error occurred while communicating with partner.')
            errorWindow.exec_()
