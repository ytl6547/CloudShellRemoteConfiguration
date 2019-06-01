from channels.generic.websocket import WebsocketConsumer
import json
import time
from WebTerm import views


class DeviceListUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        message = "hello Django channels"
        while True:
            self.send(views.getDevices())
            time.sleep(5)

    def disconnect(self, close_code):
        pass
