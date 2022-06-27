from django.db import models


# Create your models here.

class Ad(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    rating = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    date = models.CharField(max_length=255, null=True)
    url = models.URLField(unique=True)
    status = models.CharField(max_length=100, null=True)
    # created
    # updated

