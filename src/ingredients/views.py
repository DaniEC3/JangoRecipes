from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import IngredientSearchForm

# Create your views here.
@login_required
def IngredientsHome(request):
    return render(request, 'ingredients/home.html')

@login_required
def ingredient_search(request):
    form = IngredientSearchForm(request.POST or None)
    # Create the instance from forms
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        chart_type = request.POST.get('chart_type')
        print(recipe_name)
        print(chart_type)

    #pack up data to be sent to template in the context dictionary
    context={
           'form': form,
    }
    #load the sales/record.html page using the data that you just prepared
    return render(request, 'ingredients/ingredient_search.html', context)