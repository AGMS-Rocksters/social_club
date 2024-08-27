from django.db import models
from django.contrib.auth.models import AbstractUser


class Address(models.Model):
    city = models.CharField(max_length=128)
    postel_code = models.CharField(max_length=16)

    def __str__(self):
        return self.city


class User(AbstractUser):
    helper = models.BooleanField(default=False)
    seeker = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    address_id = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    


