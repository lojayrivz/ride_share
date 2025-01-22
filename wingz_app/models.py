from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    ]

    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE
    )
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='rider')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)


class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255)
    id_rider = models.ForeignKey(
        UserAccount,
        related_name="rider_rides",
        on_delete=models.CASCADE)
    id_driver = models.ForeignKey(
        UserAccount,
        related_name="driver_rides",
        on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride,
        related_name="ride_events",
        on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

