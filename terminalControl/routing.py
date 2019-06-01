from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from WebTerm.devices import DeviceListUpdateConsumer
from WebTerm import routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
            # url(r"^devices/$", DeviceListUpdateConsumer),
        )
    ),
})
