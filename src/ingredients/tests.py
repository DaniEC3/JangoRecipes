from django.test import TestCase
from .forms import IngredientSearchForm

# Create your tests here.

class IngredientSearchFormTest(TestCase):
    def test_form_valid(self):
        form = IngredientSearchForm(data={'ingredient_name': 'test'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = IngredientSearchForm(data={'ingredient_name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ingredient_name'], ['This field is required.'])