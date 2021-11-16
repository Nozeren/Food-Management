from django.contrib import admin

# Register your models here.
from .models import Ingredient, Category, To_buy

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(To_buy)
