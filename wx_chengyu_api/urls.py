from django import urls
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('battle/init', views.init, name='init'),
    path('battle', views.battle, name='battle'),
]
