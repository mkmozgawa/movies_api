from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    pass


class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    genre = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    runtime = models.CharField(max_length=10)
    body = models.JSONField(max_length=4096, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
