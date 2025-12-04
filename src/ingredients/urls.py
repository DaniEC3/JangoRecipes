from django.urls import path
from .views import IngredientsHome
# from .views import Details

app_name = 'ingredients'
urlpatterns = [
    path('', IngredientsHome, name='home'),
    # path('ingredient/<int:id>', Details, name='detail'),
]

