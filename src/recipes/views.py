from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
class Home(LoginRequiredMixin, ListView):
   model = Recipe
   template_name = 'recipes/home.html'

@login_required
def Details(request, id):
   recipe = get_object_or_404(Recipe, pk=id)
   return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})