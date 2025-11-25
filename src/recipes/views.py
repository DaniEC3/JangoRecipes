from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.
def home(request):
   return render(request, 'recipes/home.html')

def details(request, id):
   recipe = get_object_or_404(Recipe, pk=id)
   return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})