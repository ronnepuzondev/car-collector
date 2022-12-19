from django.db import models
from django.urls import reverse

# Create your models here.
# Add the Car class & list and view function below the imports

SERVICE = (
    ('O', 'Oil Change'),
    ('C', 'Car Wash'),
    ('R', 'Repair')
)

class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})

class Service(models.Model):
    date = models.DateField()
    service = models.CharField(
        max_length=1,
    # add the 'choices' field option
        choices=SERVICE,
    # set the default value for meal to be 'B'
        default=SERVICE[0][0]
  )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_service_display()} on {self.date}"