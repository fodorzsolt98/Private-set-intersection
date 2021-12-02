from time import sleep
from threading import Thread
import socket
import json


class NetworkInterface:
    def __init__(self, port, serverMaxConnection = 20, bufferSize = 2048):
        self.serverIp = '127.0.0.1'  # '0.0.0.0'
        self.serverPort = port
        self.serverMaxConnection = serverMaxConnection
        self.bufferSize = bufferSize
        self.server = self.initServer()
        self.runingServer = None
        self.__serverRun = False
        self.__clientServices = []

    def socketInit(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return soc

    def initServer(self):
        server = self.socketInit()
        server.bind((self.serverIp, self.serverPort))
        server.listen(self.serverMaxConnection)
        return server

    def jsonToBytes(self, message):
        return json.dumps(message).encode('utf-8')

    def bytesToJson(self, message):
        return json.loads(message.decode('utf-8'))

    def startServer(self):
        if not self.__serverRun:
            self.__serverRun = True
            self.runingServer = Thread(target=self.serverService)
            self.runingServer.start()

    def stopServer(self):
        if self.runingServer:
            self.__serverRun = False
            self.runingServer.join()
            for clientService in self.__clientServices:
                clientService.join()

    def clientService(self, conn, ip, port):
        print(conn.recv(self.bufferSize).decode('utf-8'))
        conn.close()

    def serverService(self):
        while self.__serverRun:
            try:
                print(f'server is on, active client serives {len(self.__clientServices)}')
                self.server.settimeout(5)
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
