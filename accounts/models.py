# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    too_user = models.TextField(max_length=500, blank=True)
    too_secret = models.CharField(max_length=30, blank=True)

    # add additional fields in here

    def __str__(self):
        return self.username
