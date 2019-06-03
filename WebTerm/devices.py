from channels.generic.websocket import WebsocketConsumer
import json
import time
from WebTerm import views
# from django.dispatch import receiver
#
# from channels_presence.signals import presence_changed

class DeviceListUpdateConsumer(WebsocketConsumer):
    connected = False

    def checkDNACUpdate(self):
        while self.connected:
            print(self.connected)
            try:
                self.send(views.getDevices())
            except:
                self.connected = False
            time.sleep(300)

    def connect(self):
        self.accept()
        self.connected = True
        self.checkDNACUpdate()

    def disconnect(self, close_code):
        print(close_code)
        self.connected = False
        print(self.connected)
        pass
