from channels.generic.websocket import WebsocketConsumer
import time
from WebTerm import views


class DeviceListUpdateConsumer(WebsocketConsumer):
    connected = False

    def checkDNACUpdate(self):
        while self.connected:
            try:
                self.send(views.getDevices())
            except:
                # print("Exception")
                break

            time.sleep(300)

    def connect(self):
        self.accept()
        self.connected = True
        self.checkDNACUpdate()

    def disconnect(self, message):
        print(message)
        self.connected = False
        print(self.connected)
        pass
