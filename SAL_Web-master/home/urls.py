from django.conf.urls import url
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('setting', views.setting, name='setting'),
    path('logs', views.logs, name='logs'),
]
