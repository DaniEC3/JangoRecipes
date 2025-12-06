from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import IngredientSearchForm
from .models import Ingredient
import pandas as pd
from pandas import DataFrame
from .utils import get_chart

# Create your views here.
@login_required
def IngredientsHome(request):
    return render(request, 'ingredients/home.html')

@login_required
def ingredient_search(request):
    form = IngredientSearchForm(request.POST or None)
    ingredients_df = None     #initialize dataframe to None
    chart = None
    # Create the instance from forms
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        chart_type = request.POST.get('chart_type')

        qs = Ingredient.objects.filter(name__icontains=ingredient_name)
        if qs.exists():
            ingredients_df = DataFrame(qs.values())
            chart=get_chart(chart_type, ingredients_df, labels=ingredients_df['quantity'].values)
            ingredients_df = ingredients_df.to_html()
    context={
           'form': form,
           'ingredients_df': ingredients_df,
           'chart': chart
    }
    #load the sales/record.html page using the data that you just prepared
    return render(request, 'ingredients/ingredient_search.html', context)