from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("barbers/", views.barbers, name="barbers"),
    path("book/", views.book, name="book"),
    path("contact/", views.contact, name="contact"),
]
