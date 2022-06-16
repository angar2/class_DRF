from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    path('', views.UserView.as_view()), # as_view: class base view일 경우
]