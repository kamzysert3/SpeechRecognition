from django.db import models

# Create your models here.
class TextModel(models.Model):
    text_data = models.TextField()
