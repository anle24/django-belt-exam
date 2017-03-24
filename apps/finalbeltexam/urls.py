from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^quotes$', views.home),
    url(r'^logout$', views.logout),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^removefavorite/(?P<id>\d+)$', views.removefavorite),
    url(r'^postquote$', views.quote),
    url(r'^users/(?P<id>\d+)$', views.userquotes)
]
