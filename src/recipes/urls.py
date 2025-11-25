from django.urls import path
from .views import home
from .views import details

app_name = 'recipes'
urlpatterns = [
   path('', home),
   path('recipe/<int:id>', details),
]  