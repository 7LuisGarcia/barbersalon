from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils import timezone

from .models import Appointment
from .forms import AppointmentForm


def home(request):
    return render(request, "shop/home.html")


def services(request):
    return render(request, "shop/services.html")


def barbers(request):
    return render(request, "shop/barbers.html")


def contact(request):
    return render(request, "shop/contact.html")


def appointment_list(request):
    appointments = Appointment.objects.all().order_by("appointment_date", "appointment_time")
    return render(request, "shop/appointments.html", {
        "appointments": appointments,
        "today": timezone.now().date(),
    })


def book(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]
            barber_name = form.cleaned_data["barber_name"]

            already_booked = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                barber_name=barber_name,
            ).exists()

            if already_booked:
                messages.error(request, "That time slot is already taken. Please choose another.")
            else:
                form.save()
                messages.success(request, "Appointment booked successfully!")
                return redirect("shop:home")
    else:
        form = AppointmentForm()

    return render(request, "shop/book.html", {"form": form})


def delete_appointment(request, pk):
    if request.method == "POST":
        get_object_or_404(Appointment, pk=pk).delete()
        return JsonResponse({"ok": True})
    return HttpResponseNotAllowed(["POST"])
    