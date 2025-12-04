from django import forms

CHART_CHOICES = (
    ('#1','Bar Chart'),
    ('#2','Line Chart'),
    ('#3','Pie Chart'),
)

class IngredientSearchForm(forms.Form): 
   ingredient_name = forms.CharField(max_length=120)
   chart_type = forms.ChoiceField(choices=CHART_CHOICES)
