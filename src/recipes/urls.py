from django.urls import path
from .views import Home
from .views import Details

app_name = 'recipes'
urlpatterns = [
   path('', Home.as_view(), name='home'),
   path('recipe/<int:id>', Details, name='detail'),
]  