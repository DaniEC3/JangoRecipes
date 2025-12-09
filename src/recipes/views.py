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
        
        # Add the search form to context - only populate with POST data on POST requests
        if self.request.method == 'POST':
            context['form'] = RecipeSearchForm(self.request.POST)
        else:
            context['form'] = RecipeSearchForm()
        
        # Initialize chart and dataframe
        context['recipes'] = None
        
        # If POST request, process the search and generate chart
        if self.request.method == 'POST':
            recipe_name = self.request.POST.get('recipe_name')
            
            # Get the filtered queryset - keep as queryset to preserve properties like difficulty
            qs = self.get_queryset().prefetch_related('ingredients')
            if qs.exists():
                context['recipes'] = qs
        
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
    ingredient_links = recipe.recipe_ingredients.select_related('ingredient')

    # Build dataframe for chart generation if ingredients exist
    ingredients_df = DataFrame(
        list(
            ingredient_links.values(
                'ingredient__name',
                'ingredient__calories',
                'ingredient__price',
                'quantity'
            )
        )
    ) if ingredient_links.exists() else DataFrame()

    form = ChartForm(request.POST or None)
    if request.method == 'POST' and ingredients_df.shape[0] > 0:
        chart_type = request.POST.get('chart_type')
        chart = get_chart(chart_type, ingredients_df, labels=ingredients_df['ingredient__name'].values)

    context = {
        'recipe': recipe,
        'ingredient_links': ingredient_links,
        'chart': chart,
        'form': form,
    }
    return render(request, 'recipes/recipe_detail.html', context)