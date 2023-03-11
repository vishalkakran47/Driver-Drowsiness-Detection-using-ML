# from django.db import models
# from __future__ import unicode_literals
from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class gender_type(Enum):  # A subclass of Enum
    M = "Male"
    F = "Female"


class country_type(Enum):  # A subclass of Enum
    In = "India"
    Ca = "Canada"
    US = "USA"


class vehicle_list_type(Enum):  # A subclass of Enum
    Car = "Car"
    Bus = "Bus"
    Truck = "Truck"


class Driver(models.Model):
    #id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50, primary_key=True)
    mobile_number = models.IntegerField()
    four_digit_pin = models.IntegerField()
    confirm_four_digit_pin = models.IntegerField()
    daily_driving_hours = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    gender = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in gender_type])
    date_of_birth = models.DateField
    vehicle_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in vehicle_list_type])

    class Meta:
        db_table = "driver_details"
