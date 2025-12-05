from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import IngredientSearchForm
from .models import Ingredient

# Create your views here.
@login_required
def IngredientsHome(request):
    return render(request, 'ingredients/home.html')

@login_required
def ingredient_search(request):
    form = IngredientSearchForm(request.POST or None)
    # Create the instance from forms
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        chart_type = request.POST.get('chart_type')

        # print ('Exploring querysets:')
        # # .objects - Django's model manager (gives you access to database queries)
        # print ('Case 1: Output of Ingredient.objects.all()')
        # ingredient = Ingredient.objects.all()
        # print(ingredient)

        # print ('Case 2: Output of Ingredient.objects.filter(name__icontains=ingredient_name)')
        # ingredient = Ingredient.objects.filter(name__icontains=ingredient_name)
        # print (ingredient)

        # print ('Case 3: Output of ingredient.values')
        # print (ingredient.values())

        # print ('Case 4: Output of ingredient.values_list()')
        # print (ingredient.values_list())

        # print ('Case 5: Output of Ingredient.objects.get(id=1)')
        # obj = Ingredient.objects.get(id=1)
        # print (obj)
    #pack up data to be sent to template in the context dictionary
    context={
           'form': form,
        #    'ingredient': ingredient,
    }
    #load the sales/record.html page using the data that you just prepared
    return render(request, 'ingredients/ingredient_search.html', context)