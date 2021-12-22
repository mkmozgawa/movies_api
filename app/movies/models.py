from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    pass


class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, default=None)
    genre = models.CharField(max_length=255)
    year = models.CharField(max_length=9)
    runtime = models.CharField(max_length=10)
    body = models.JSONField(max_length=4096, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class MovieComment(models.Model):
    text = models.CharField(max_length=2000, null=False, blank=False, default=None)
    movie_id = models.IntegerField(null=False, blank=False, default=None)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'
