from django.conf.urls import url, include
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wall$', views.wall),
    url(r'^logout$', views.logout),
    url(r'^create_message$', views.create_message),
    url(r'^create_comments$)
]