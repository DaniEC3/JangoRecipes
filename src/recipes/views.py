from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.views.generic import ListView

# Create your views here.
class Home(ListView):
   model = Recipe
   template_name = 'recipes/home.html'

def Details(request, id):
   recipe = get_object_or_404(Recipe, pk=id)
   return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})