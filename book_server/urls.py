# -*- coding:utf-8 -*-

from django.conf.urls import url
from book_server import views

urlpatterns = [
    url(r'^book_list', views.book_list),
    url(r'^book_detail', views.book_detail),
    url(r'^app_state', views.app_state),

]
