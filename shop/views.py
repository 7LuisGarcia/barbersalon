from django.shortcuts import render, redirect
from .forms import AppointmentForm


def home(request):
    return render(request, "shop/home.html")


def services(request):
    return render(request, "shop/services.html")


def barbers(request):
    return render(request, "shop/barbers.html")


def book(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shop:home")
    else:
        form = AppointmentForm()

    return render(request, "shop/book.html", {"form": form})


def contact(request):
    return render(request, "shop/contact.html")

# Create your views here.
