from django.urls import path
from myAPI import views

urlpatterns = [
    path('', views.myAPI, name='myAPI'),
]
