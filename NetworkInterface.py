from Client import Client
from MessageCipher import MessageCipher
from CustomSocket import CustomSocket
from time import sleep
from threading import Thread
from Coders import bytesToJson, jsonToBytes, bytesToInt
import socket
import random
from secret_list_creator import create_points_list, compute_common_point_list, point_list_to_dictionary, point_list_from_dictionary


class NetworkInterface:
    def __init__(self, meetingHandler, port, serverMaxConnection = 20, bufferSize = 1024):
        self.serverIp = '0.0.0.0'
        self.serverPort = port
        self.serverMaxConnection = serverMaxConnection
        self.bufferSize = bufferSize
        self.meetingHandler = meetingHandler
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
        meetingTimeData = bytesToJson(client.receiveData())
        print("Receiver")
        x = client.receiveData()
        print(x)
        MeetingsPointsFromOtherParty = point_list_from_dictionary(bytesToJson(x))
        freeSlots = self.meetingHandler.createFreeSlots(meetingTimeData['weeks'], meetingTimeData['meetingLength'])
        filteredfreeSlots = self.meetingHandler.meetingsToList(self.meetingHandler.filterCollosions(self.meetingHandler.meetings, freeSlots))
        LocalMeetings = [meeting.getDateAndTime() for meeting in filteredfreeSlots]  # These are the free slots to send, please change this to the DH encryption.
        private_input = random.randint(1, 100)
        LocalMeetingsPoints, LocalMeetingsTuples = create_points_list(LocalMeetings, private_input)
        client.sendData(jsonToBytes(point_list_to_dictionary(LocalMeetingsPoints)))
        CommonMeetingsPointsFromOtherParty = compute_common_point_list(MeetingsPointsFromOtherParty, private_input)
        client.sendData(jsonToBytes(point_list_to_dictionary(CommonMeetingsPointsFromOtherParty)))  # These are A's meetings they need to be DH encrypted with B's key.
        selectedMeetingPosition = bytesToInt(client.receiveData())
        meetingTextData = bytesToJson(client.receiveData())
        client.bye()
        selectedMeeting = filteredfreeSlots[selectedMeetingPosition]
        selectedMeeting.title = meetingTextData['title']
        selectedMeeting.description = meetingTextData['description']
        self.meetingHandler.addMeeting(selectedMeeting)

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
