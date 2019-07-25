from channels.generic.websocket import WebsocketConsumer
import time
from WebTerm import views
from threading import Thread
import json

class DeviceListUpdateConsumer(WebsocketConsumer):
    connected = False

    def checkDNACUpdate(self):
        while self.connected:
            try:
                result = views.getDevices()
                self.send(json.dumps(result))
            except:
                break

            time.sleep(300)

    def connect(self):
        self.accept()
        self.connected = True
        t = Thread(target=self.checkDNACUpdate)
        t.start()
        print("Started to check DNAC updates for a client")

    def disconnect(self, close_code):
        self.connected = False
        print("Stopped checking DNAC updates for a client")
        pass
