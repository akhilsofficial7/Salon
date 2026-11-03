from django.db import models

class StylistDb(models.Model):
    stylist_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    salon_branch = models.CharField(max_length=200)
    service_fee = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.stylist_name


class BookingDb(models.Model):
    client_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    stylist_id = models.IntegerField()
    booking_date = models.DateField()
    token_number = models.PositiveIntegerField(editable=False, null=True)
    booking_time = models.TimeField(editable=False, null=True)
    service_required = models.TextField()
    status = models.CharField(max_length=200, default="pending")
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name