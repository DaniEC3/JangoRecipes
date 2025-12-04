from django.urls import path
from .views import IngredientsHome, ingredient_search

app_name = 'ingredients'
urlpatterns = [
    path('', IngredientsHome, name='home'),
    path('search/', ingredient_search, name='search'),
]

