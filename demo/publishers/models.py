from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=220)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
