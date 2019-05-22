from django.conf.urls import url
from WebTerm import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^terminal/$', views.terminal, name='terminal')
]