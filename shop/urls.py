from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("barbers/", views.barbers, name="barbers"),
    path("contact/", views.contact, name="contact"),
    path("appointments/", views.appointment_list, name="appointments"),
    path("appointments/<int:pk>/delete/", views.delete_appointment, name="appointment_delete"),
    path("book/", views.book, name="book"),
]
