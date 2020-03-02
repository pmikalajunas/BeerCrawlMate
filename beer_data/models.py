from django.db import models

# Id of a home (starting) node.
HOME_NODE_ID = -2

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

    # Returns a list of beers that each brewery in a lsit of nodes contains.
    def get_beers(nodes):
        beers = []
        for node in nodes:
            if node.id == HOME_NODE_ID:
                continue
            brewery = Brewery.objects.filter(id=node.id)[0]
            brewery_beers = Beer.objects.filter(brewery=brewery)
            beers += brewery_beers
        return beers


