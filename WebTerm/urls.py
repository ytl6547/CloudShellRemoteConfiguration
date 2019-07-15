from django.conf.urls import url
from WebTerm import views
# from WebTerm.devices import DeviceListUpdateConsumer

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^terminal/$', views.terminal, name='terminal'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^remove/$', views.removeDevice, name='remove'),

    # url(r'^devices/$', views.devices, name='devices')
]