from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=100, null=False,blank=False)
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    user = models.ForeignKey(User,related_name="ingredient",on_delete=models.CASCADE, null=True)
    name= models.CharField(max_length=200, null=False,blank=False)
    quantity = models.IntegerField(null= False,blank=False)
    image = models.ImageField(default=f"{name}.png")
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)
    
    def __str__(self):
        return self.name

class To_buy(models.Model):
    user = models.ForeignKey(User,related_name="to_buy",on_delete=models.CASCADE, null=True)
    name= models.CharField(max_length=200, null=False,blank=False)
    quantity = models.IntegerField(default= 1,null= False,blank=False)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)
    
    def __str__(self):
        return self.name