from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Difficulty level choices - constrains what values can be stored
DIFFICULTY_CHOICES = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
)

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cooking_time = models.IntegerField(help_text='in minutes', default=0)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    difficulty = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES,
        default='Easy'
    )

    def __str__(self):
        return self.name  