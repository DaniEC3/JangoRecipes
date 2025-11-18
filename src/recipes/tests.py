from django.test import TestCase
from .models import Recipe


# Create your tests here.

class RecipeModelTest(TestCase):
    def setUpTestData(self):
        Recipe.objects.create(
            title="Test Recipe",
            description="This is a test recipe.",
            ingredients="Ingredient1, Ingredient2",
            instructions="Step 1: Do this. Step 2: Do that."
        )
    def test_title_label(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # Get the metadata for the 'title' field and use it to query its data
        field_label = recipe. _meta.get_field('title').verbose_name
        # Compare the value to the expected result
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)