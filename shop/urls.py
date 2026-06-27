from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("barbers/", views.barbers, name="barbers"),        # ← need to add barbers view
    path("contact/", views.contact, name="contact"),
    path("appointments/", views.appointments, name="appointments"),  # was appointment_list
    path("appointments/<int:pk>/delete/", views.delete_appointment, name="appointment_delete"),
    path("book/", views.book, name="book"),                 # removed duplicate
    path("book/success/", views.booking_success, name="booking_success"),
]