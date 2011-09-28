from django.db import models

class PythonBrasil(models.Model):
    place = models.CharField(max_length=255)
