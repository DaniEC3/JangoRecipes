from django.test import TestCase
from .forms import IngredientSearchForm

# Create your tests here.

class IngredientSearchFormTest(TestCase):
    
    def test_form_valid(self):
        """Test that a form with valid data is valid"""
        form = IngredientSearchForm(data={'ingredient_name': 'test', 'chart_type': '#1'})
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_missing_ingredient(self):
        """Test that a form with empty ingredient_name is invalid"""
        form = IngredientSearchForm(data={'ingredient_name': '', 'chart_type': '#1'})
        self.assertFalse(form.is_valid())
        self.assertIn('ingredient_name', form.errors)
    
    def test_form_invalid_missing_chart_type(self):
        """Test that a form without chart_type is invalid"""
        form = IngredientSearchForm(data={'ingredient_name': 'test'})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)
    
    def test_chart_form_invalid_choice(self):
        """Test that a form with invalid chart_type is invalid"""
        form = IngredientSearchForm(data={'ingredient_name': 'test', 'chart_type': 'invalid'})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)
        