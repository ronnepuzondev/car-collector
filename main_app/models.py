from django.db import models
from django.urls import reverse

# Create your models here.
# Add the Car class & list and view function below the imports
class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})