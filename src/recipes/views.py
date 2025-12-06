from django.shortcuts import render, get_object_or_404
from .models import Recipe
from .models import Ingredient
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm, ChartForm
import pandas as pd
from pandas import DataFrame
from .utils import get_chart

# Create your views here.
class Home(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    
    def get_queryset(self):
        """
        Override get_queryset to filter recipes based on search input.
        If there's a POST request with a recipe name, filter the queryset.
        Otherwise, return all recipes.
        """
        queryset = super().get_queryset()
        
        if self.request.method == 'POST':
            recipe_name = self.request.POST.get('recipe_name')
            if recipe_name:
                queryset = queryset.filter(name__icontains=recipe_name)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add the search form and chart data to the context.
        """
        context = super().get_context_data(**kwargs)  # Gets default context with 'object_list'
        
        # Add the search form to context
        context['form'] = RecipeSearchForm(self.request.POST or None)
        
        # Initialize chart and dataframe
        context['recipes'] = None
        
        # If POST request, process the search and generate chart
        if self.request.method == 'POST':
            recipe_name = self.request.POST.get('recipe_name')
            
            # Get the filtered queryset
            qs = self.get_queryset()
            
            if qs.exists():
                if qs.values() != None:
                    recipes = list(qs.values())
                else:
                    recipes = list(Recipe.objects.all().values())
                context['recipes'] = recipes
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests (form submissions).
        This allows the ListView to handle POST requests for search.
        """
        # Call get() to render the page with filtered results
        return self.get(request, *args, **kwargs)

@login_required
def Details(request, id): 
    chart = None
    recipe = get_object_or_404(Recipe, pk=id)
    ingredients_qs = recipe.ingredients.all()

    # Build dataframe for chart generation if ingredients exist
    ingredients_df = DataFrame(list(ingredients_qs.values())) if ingredients_qs.exists() else DataFrame()

    form = ChartForm(request.POST or None)
    if request.method == 'POST' and ingredients_df.shape[0] > 0:
        chart_type = request.POST.get('chart_type')
        chart = get_chart(chart_type, ingredients_df, labels=ingredients_df['name'].values)

    context = {
        'recipe': recipe,
        'ingredients': ingredients_qs,
        'chart': chart,
        'form': form,
    }
    return render(request, 'recipes/recipe_detail.html', context)