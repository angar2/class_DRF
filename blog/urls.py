from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.ArticleView.as_view()), # as_view: class base view일 경우
]