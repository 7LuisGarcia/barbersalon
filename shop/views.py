from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.db import IntegrityError
from datetime import timedelta

from .models import Appointment
from .forms import AppointmentForm


def home(request):
    return render(request, "shop/home.html")


def services(request):
    return render(request, "shop/services.html")


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    return render(request, "shop/contact.html")


def gallery(request):
    return render(request, "shop/gallery.html")

def barbers(request):
    return render(request, "shop/barbers.html")


def book(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        appt_time = request.POST.get("appointment_time")
        if form.is_valid() and appt_time:
            appt = form.save(commit=False)
            appt.appointment_time = appt_time

            already_taken = Appointment.objects.filter(
                barber_name=appt.barber_name,
                appointment_date=appt.appointment_date,
                appointment_time=appt.appointment_time,
            ).exclude(status="cancelled").exists()

            if already_taken:
                form.add_error(None, "That time slot is already booked. Please choose a different time.")
                return render(request, "shop/book_appointment.html", {"form": form})

            try:
                appt.save()
                return redirect("shop:booking_success")
            except IntegrityError:
                form.add_error(None, "That time slot was just taken. Please choose a different time.")
                return render(request, "shop/book_appointment.html", {"form": form})
    else:
        form = AppointmentForm()
    return render(request, "shop/book_appointment.html", {"form": form})


def booking_success(request):
    return render(request, "shop/booking_success.html")


def appointments(request):
    all_appointments = Appointment.objects.all().order_by("appointment_date", "appointment_time")
    today = timezone.now().date()
    return render(request, "shop/appointments.html", {
        "appointments": all_appointments,
        "today": today,
    })


def delete_appointment(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return JsonResponse({"ok": True})


def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if not appointment.can_cancel_or_reschedule():
        messages.error(request, "Cancellations must be made at least 24 hours before your appointment.")
        return redirect("shop:appointments")
    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Your appointment has been cancelled.")
    return redirect("shop:appointments")