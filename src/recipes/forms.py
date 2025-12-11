from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CHART_CHOICES = (
    ('#1','Ingredients Prices'),
    ('#2','Ingredients Calories'),
    ('#3','Ingredients Quantity Distribution'),
)

class RecipeSearchForm(forms.Form): 
   recipe_name = forms.CharField(max_length=120)

class ChartForm(forms.Form): 
   chart_type = forms.ChoiceField(choices=CHART_CHOICES)