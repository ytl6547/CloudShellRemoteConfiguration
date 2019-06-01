from django.conf.urls import url

from WebTerm.devices import DeviceListUpdateConsumer

websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r"^ws/devices/$", DeviceListUpdateConsumer),
]