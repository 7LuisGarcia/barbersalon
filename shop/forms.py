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
        exclude = ['status', 'created_at', 'appointment_time']
        labels = {
            'customer_name': 'Nombre',
            'customer_phone': 'Teléfono del cliente',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'service': 'Servicio',
            'barber_name': 'Barbero',
            'appointment_date': 'Fecha',
            'notes': 'Notas',
            'payment_method': 'Método de pago',
            'payment_screenshot': 'Captura del pago por Zelle',
        }
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_screenshot': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages.update({
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce un valor válido.',
                'invalid_choice': 'Selecciona una opción válida.',
                'max_length': 'Usa como máximo %(limit_value)s caracteres (introdujiste %(show_value)s).',
            })
        self.fields['email'].error_messages['invalid'] = 'Introduce un correo electrónico válido.'
        self.fields['appointment_date'].error_messages['invalid'] = 'Introduce una fecha válida.'
        self.fields['payment_screenshot'].error_messages.update({
            'invalid': 'No se pudo leer el archivo. Selecciona otra imagen.',
            'invalid_image': 'Sube una imagen válida.',
            'empty': 'El archivo está vacío.',
        })
        self.fields['service'].choices = [
            ('', 'Selecciona un servicio'),
            ('Haircut', 'Corte de cabello'),
            ('Beard Trim', 'Arreglo de barba'),
            ('Haircut + Beard', 'Corte y barba'),
            ('Kids Cut', 'Corte infantil'),
            ('Fade', 'Degradado'),
        ]
        self.fields['barber_name'].choices = [
            ('', 'Selecciona un barbero'),
            ('Gina', 'Gina'),
            ('Tere', 'Tere'),
            ('Third', 'Tercer barbero'),
        ]
        self.fields['payment_method'].choices = [
            ('cash', 'Efectivo'),
            ('zelle', 'Zelle'),
        ]

    def clean_payment_screenshot(self):
        screenshot = self.cleaned_data.get('payment_screenshot')
        if not screenshot:
            raise forms.ValidationError("Debes subir una captura del pago por Zelle para reservar.")
        return screenshot
