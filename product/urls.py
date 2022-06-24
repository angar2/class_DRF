from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('', views.ProductView.as_view()), # as_view: class base view일 경우
    path('<product_id>/',views.ProductView.as_view())
]