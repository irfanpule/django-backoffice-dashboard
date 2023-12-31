from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    instagram = models.URLField()

    def __str__(self):
        return self.name
