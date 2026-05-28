from django.db import models


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ("Haircut", "Haircut"),
        ("Beard Trim", "Beard Trim"),
        ("Haircut + Beard", "Haircut + Beard"),
        ("Kids Cut", "Kids Cut"),
        ("Fade", "Fade"),
    ]

    BARBER_CHOICES = [
        ("Gina", "Gina"),
        ("Tere", "Tere"),
        ("Third", "Third"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    barber = models.CharField(max_length=100, choices=BARBER_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)

    payment_method = models.CharField(
    max_length=20,
    choices=[
        ("cash", "Cash"),
        ("zelle", "Zelle"),
    ],
    default="cash"
)

    def __str__(self):
        return f"{self.name} - {self.service}"