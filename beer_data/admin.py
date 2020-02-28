from django.contrib import admin

from .models import *

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Category)