import pandas as pd
import os

from .models import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


UNKNOWN_BREWERY = -1
UNKNOWN_CATEGORY = -1

def read_csv_data():
    preprocess_database()
    read_brewery_data()
    read_categories()
    read_beer_data()
    read_geocodes()


# Creates DB entries for unknown categories and breweries.
def preprocess_database():
    if not Brewery.objects.filter(id=UNKNOWN_BREWERY).exists():
        Brewery.objects.create(
            id=-1,
            name="Unknown brewery",
            beer_count=0
        )
    if not Category.objects.filter(id=UNKNOWN_CATEGORY).exists():  
        Category.objects.create(
            id=-1,
            name="Unknown category"
        )


def read_brewery_data():
    csv = pd.read_csv(os.path.join(BASE_DIR, 'beer_data/csv_data/breweries.csv'), usecols=['id', 'name'])
    for row in csv.itertuples():
        # Avoid adding brewery that already exists.
        if Brewery.objects.filter(id=row.id).exists():
            continue
        Brewery.objects.create(
            id = row.id,
            name = row.name
        )


def read_categories():
    csv = pd.read_csv(os.path.join(BASE_DIR, 'beer_data/csv_data/categories.csv'), usecols=['id', 'cat_name'])
    for row in csv.itertuples():
        # Avoid adding category that already exists.
        if Category.objects.filter(id=row.id).exists():
            continue
        Category.objects.create(
            id = row.id,
            name = row.cat_name
        )


def read_geocodes():
    csv = pd.read_csv(os.path.join(BASE_DIR, 'beer_data/csv_data/geocodes.csv'), usecols=['brewery_id', 'latitude', 'longitude'])    
    for row in csv.itertuples():
        # Check if associated brewery exists.
        # If not, proceed with next entry, not every brewery has a geocode.
        try:    
            brewery = Brewery.objects.filter(id=row.brewery_id)[0]
        except:
            continue
        # Update brewery's location.
        brewery.latitude = row.latitude
        brewery.longitude = row.longitude
        brewery.save()



def read_beer_data():
    csv = pd.read_csv(os.path.join(BASE_DIR, 'beer_data/csv_data/beers.csv'), usecols=['id', 'brewery_id', 'name', 'cat_id'])
    for row in csv.itertuples():
        # Avoid adding beer that already exists.
        if Beer.objects.filter(id=row.id).exists():
            continue
        # Check if there is an associated brewery, if not assign to unknown.
        try:
            beer_brewery = Brewery.objects.filter(id=row.brewery_id)[0]
        except:
            beer_brewery = Brewery.objects.filter(id=UNKNOWN_BREWERY)[0]
        # Check if there is an associated category, if not assign to unknown.            
        try:
            beer_category = Category.objects.filter(id=row.cat_id)[0]
        except:
            beer_category = Category.objects.filter(id=UNKNOWN_CATEGORY)[0]        
        Beer.objects.create(
            id = row.id,
            brewery = beer_brewery,
            name = row.name,
            category = beer_category
        )
        updateBreweryBeerCount(beer_brewery)


def updateBreweryBeerCount(beer_brewery):
    beer_brewery.beer_count += 1
    beer_brewery.save()
