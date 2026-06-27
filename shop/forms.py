from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "customer_name",
            "email",
            "phone",
            "service",
            "barber_name",
            "appointment_date",
            "appointment_time",
            "notes",
            "payment_method",
        ]

        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

# forms.py
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['status', 'created_at', 'appointment_time']  # add this
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_screenshot': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean_payment_screenshot(self):
        screenshot = self.cleaned_data.get('payment_screenshot')
        if not screenshot:
            raise forms.ValidationError("You must upload a Zelle payment screenshot to book.")
        return screenshot        