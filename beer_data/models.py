from django.db import models


class Brewery(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default='Unknown brewery')
    beer_count = models.IntegerField(default=0)
    latitude = models.FloatField(default=-1)
    longitude = models.FloatField(default=-1)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default='Unknown Category')


class Beer(models.Model):
    id = models.IntegerField(primary_key=True)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='Unknown beer')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
