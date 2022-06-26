from django.db import models


# Create your models here.

class Ad(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    rating = models.CharField(max_length=255)
    description = models.TextField()
    date = models.CharField(max_length=255)
    url = models.URLField()
    status = models.CharField(max_length=100)
