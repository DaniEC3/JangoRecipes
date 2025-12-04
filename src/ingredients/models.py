from django.db import models
from django.urls import reverse

# Create your models here.

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
    