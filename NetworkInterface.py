from Client import Client
from MessageCipher import MessageCipher
from CustomSocket import CustomSocket
from time import sleep
from threading import Thread
from Coders import bytesToJson
from MessageWindows import InformationMessageWindowWithButtons, Ok, Cancel
import socket


class NetworkInterface:
    def __init__(self, port, serverMaxConnection = 20, bufferSize = 2048):
        self.serverIp = '0.0.0.0'
        self.serverPort = port
        self.serverMaxConnection = serverMaxConnection
        self.bufferSize = bufferSize
        self.server = self.initServer()
        self.cipher = MessageCipher()
        self.runningServer = None
        self.__serverRun = False
        self.__clientServices = []

    def socketInit(self):
        #soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc = CustomSocket(self.bufferSize, socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return soc

    def initServer(self):
        server = self.socketInit()
        server.bind((self.serverIp, self.serverPort))
        server.listen(self.serverMaxConnection)
        return server

    def createClient(self, ip, port):
        conn = self.socketInit()
        conn.connect((ip, port))
        conn.sendAllWithByteCount(self.cipher.asymmetricKey.publickey().exportKey('PEM'))
        return Client(conn, self.cipher, MessageCipher(conn.recvAllWithByteCount()))

    def startServer(self):
        if not self.__serverRun:
            self.__serverRun = True
            self.runningServer = Thread(target=self.serverService)
            self.runningServer.start()

    def stopServer(self):
        if self.runningServer:
            self.__serverRun = False
            self.runningServer.join()
            for clientService in self.__clientServices:
                clientService.join()

    def clientService(self, conn, ip, port):
        client = Client(conn, self.cipher, MessageCipher(conn.recvAllWithByteCount()))
        conn.sendAllWithByteCount(self.cipher.asymmetricKey.publickey().exportKey('PEM'))
        incommingData = bytesToJson(client.receiveData())
        weeks = incommingData['weeks']
        meetingLength = incommingData['meetingLength']
        print(weeks)
        print(meetingLength)
        #A's encrypted meetings will be received here
        print(client.receiveData())
        client.sendData(b'B\'s encrypted meetings will be sent here')
        client.sendData(b'A\'s encrypted meetings with B will be sent here')
        # The position of the chosen meeting, the name and title will be received here
        print(client.receiveData())
        # receive B's acceptance
        print(client.receiveText())
        print('connection is closed')
        client.bye()

    def serverService(self):
        while self.__serverRun:
            try:
                print(f'server is on, active client serives {len(self.__clientServices)}')
                self.server.settimeout(1)
                (conn, (ip, port)) = self.server.accept()
                service = Thread(target=self.clientService, args=[conn, ip, port])
                service.start()
                self.__clientServices.append(service)
            except socket.timeout:
                pass
            for clientService in self.__clientServices:
                if not clientService.is_alive():
                    clientService.join()
                    self.__clientServices.remove(clientService)
            sleep(0.1)
