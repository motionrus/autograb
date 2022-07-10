from django.db import models
import re


class Ad(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    rating = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    date = models.CharField(max_length=255, null=True)
    url = models.URLField(unique=True)
    status = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rating_number(self):
        try:
            if self.rating:
                sign = -1 if "дешевле" in self.rating else 1
                return int(re.sub(r'\D+', '', self.rating)) * sign
        except ValueError:
            pass
        return 0

    @rating_number.setter
    def rating_number(self, value):
        pass


class Parser(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    percentage = models.IntegerField(default=0)
    status = models.CharField(max_length=255)
