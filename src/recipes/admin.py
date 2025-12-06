from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient

# Register your models here.
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'quantity']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'cooking_time', 'difficulty', 'user']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
