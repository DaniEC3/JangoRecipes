from django import forms

CHART_CHOICES = (
    ('#1','Bar Chart'),
    ('#2','Line Chart'),
    ('#3','Pie Chart'),
)

class RecipeSearchForm(forms.Form): 
   recipe_name = forms.CharField(max_length=120)
class ChartForm(forms.Form): 
   chart_type = forms.ChoiceField(choices=CHART_CHOICES)
