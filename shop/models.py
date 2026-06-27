from django.db import models
from django.utils import timezone
from datetime import timedelta


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

    STATUS_CHOICES = [
        ("pending", "Pending Payment Verification"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("zelle", "Zelle"),
    ]

    customer_name      = models.CharField(max_length=100)
    customer_phone     = models.CharField(max_length=20)
    email              = models.EmailField(blank=True, null=True)
    phone              = models.CharField(max_length=20, blank=True)
    service            = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    barber_name        = models.CharField(max_length=100, choices=BARBER_CHOICES)
    appointment_date   = models.DateField()
    appointment_time   = models.TimeField()
    notes              = models.TextField(blank=True, null=True)
    payment_method     = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cash")
    payment_screenshot = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_date", "appointment_time"]
        unique_together = ("barber_name", "appointment_date", "appointment_time")

    def can_cancel_or_reschedule(self):
        appointment_dt = timezone.make_aware(
            timezone.datetime.combine(self.appointment_date, self.appointment_time)
        )
        return timezone.now() < appointment_dt - timedelta(hours=24)

    def __str__(self):
        return f"{self.customer_name} — {self.appointment_date} at {self.appointment_time}"