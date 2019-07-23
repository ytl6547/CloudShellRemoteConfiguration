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
                break

            time.sleep(300)

    def connect(self):
        self.accept()
        self.connected = True
        self.checkDNACUpdate()

    def disconnect(self, close_code):
        # print(close_code)
        self.connected = False
        # print(self.connected)
        pass
