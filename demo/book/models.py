from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    publish_date = models.DateField()
    publisher = models.ForeignKey("publishers.Publisher", on_delete=models.CASCADE)
    author = models.ForeignKey("author.Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
