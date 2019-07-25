from channels.generic.websocket import WebsocketConsumer
import time
from WebTerm import views
from threading import Thread


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
        global t
        self.accept()
        self.connected = True
        t = Thread(target=self.checkDNACUpdate)
        t.start()

    def disconnect(self, close_code):
        self.connected = False
        print("Stopped checking DNAC updates for a client")
        pass
