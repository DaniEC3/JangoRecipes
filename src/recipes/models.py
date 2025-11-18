from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    ingredients = models.TextField()
    DIFFICULTY_CHOICES = [
       ('easy', 'Easy'),
       ('medium', 'Medium'),
       ('intermediate', 'Intermediate'),
       ('hard', 'Hard'),
   ]
    difficulty_level = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    instructions = models.TextField()
    

    def __str__(self):
        return self.name  