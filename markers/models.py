from django.db import models

# Create your models here.

class Story(models.Model):

    code = models.CharField(max_length=10)
    comment = models.TextField()