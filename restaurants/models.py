from statistics import mode
from xml.etree.ElementTree import tostring
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class restaurant(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    rating = models.IntegerField(default=0, verbose_name="Rating of the restaurant", validators=[MinValueValidator(0, 'It is not allowed to use negative numbers'), MaxValueValidator(4, 'The max qualification for a restaurant is 4')])
    name = models.CharField("Name of the restaurant", max_length=64)
    site = models.CharField("Web site of the restaurant", max_length=255)
    email = models.CharField("Email of the restaurant", max_length=62)
    phone = models.CharField("Phone of the restaurant", max_length=10)
    street = models.CharField("Street where is located the restaurant", max_length=35)
    city = models.CharField("City where is located the restaurant", max_length=35)
    state = models.CharField("State where is located the restaurant", max_length=35)
    lat = models.FloatField("Latitude of the location of the restaurant")
    lng  = models.FloatField("Longitude of the location of the restaurant")

    def __str__(self) -> str:
        return self.name