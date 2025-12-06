from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cooking_time = models.IntegerField(help_text='in minutes', default=0)
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredient')  # Reference Ingredient in the same app
    instructions = models.TextField()   
    pic = models.ImageField(upload_to='recipe_pics', default='no_picture.jpg')
    @property
    def difficulty(self):
        """Calculate difficulty based on cooking time and number of ingredients"""
        ingredient_count = self.ingredients.count()
        if self.cooking_time < 30 and ingredient_count <= 5:
            return 'Easy'
        elif self.cooking_time < 30 and ingredient_count > 5:
            return 'Medium'
        elif self.cooking_time >= 30 and ingredient_count <= 5:
            return 'Intermediate'
        else:
            return 'Hard'
    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id': self.pk})
    
    def __str__(self):
        return self.name  

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    calories  = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255)
    pic = models.ImageField(upload_to='ingredient_pics', default='no_picture.jpg')
    
    def get_absolute_url(self):
        return reverse('ingredients:detail', kwargs={'id': self.pk})

    def __str__(self):
        return self.name