from django.test import TestCase
from .forms import IngredientSearchForm
from .models import Ingredient

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


class IngredientModelTest(TestCase):
    """
    Test suite for Ingredient model QuerySet operations.
    These tests correspond to the QuerySet explorations in views.py
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Create test ingredients for all test methods.
        This runs once before all tests in this class.
        """
        # Create sample ingredients
        cls.flour = Ingredient.objects.create(
            name="Flour",
            calories=100,
            price=2.50,
            quantity=1000,
            supplier="Baker's Supply"
        )
        cls.sugar = Ingredient.objects.create(
            name="Sugar",
            calories=200,
            price=3.00,
            quantity=500,
            supplier="Sweet Shop"
        )
        cls.chocolate = Ingredient.objects.create(
            name="Chocolate Chips",
            calories=150,
            price=5.00,
            quantity=250,
            supplier="Chocolate Factory"
        )
    
    # Case 1: Test Ingredient.objects.all()
    def test_queryset_all(self):
        """
        Test that .all() returns all ingredients from the database.
        Equivalent to: SELECT * FROM ingredients_ingredient;
        """
        ingredients = Ingredient.objects.all()
        
        # Check that we get a QuerySet
        self.assertEqual(type(ingredients).__name__, 'QuerySet')
        
        # Check that we have all 3 ingredients
        self.assertEqual(ingredients.count(), 3)
        
        # Check that our test ingredients are in the result
        self.assertIn(self.flour, ingredients)
        self.assertIn(self.sugar, ingredients)
        self.assertIn(self.chocolate, ingredients)
    
    # Case 2: Test Ingredient.objects.filter(name__icontains=ingredient_name)
    def test_queryset_filter_by_name(self):
        """
        Test that .filter() with name__icontains performs case-insensitive search.
        The __icontains lookup does a case-insensitive LIKE query.
        """
        # Search for ingredients containing "chocolate" (case-insensitive)
        ingredients = Ingredient.objects.filter(name__icontains='chocolate')
        
        # Should find only the chocolate chips
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(ingredients.first(), self.chocolate)
        
        # Search for ingredients containing "sugar" (lowercase)
        ingredients = Ingredient.objects.filter(name__icontains='sugar')
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(ingredients.first(), self.sugar)
        
        # Search for partial match
        ingredients = Ingredient.objects.filter(name__icontains='choc')
        self.assertEqual(ingredients.count(), 1)
        
        # Search that returns no results
        ingredients = Ingredient.objects.filter(name__icontains='vanilla')
        self.assertEqual(ingredients.count(), 0)
    
    # Case 3: Test ingredient.values()
    def test_queryset_values(self):
        """
        Test that .values() returns dictionaries instead of model instances.
        Each item in the QuerySet is a dictionary with field names as keys.
        """
        ingredients = Ingredient.objects.filter(name__icontains='flour').values()
        
        # Check that we get a QuerySet
        self.assertEqual(type(ingredients).__name__, 'QuerySet')
        
        # Get the first (and only) result
        flour_dict = ingredients.first()
        
        # Check that it's a dictionary
        self.assertIsInstance(flour_dict, dict)
        
        # Check that it has the expected keys
        self.assertIn('id', flour_dict)
        self.assertIn('name', flour_dict)
        self.assertIn('calories', flour_dict)
        self.assertIn('price', flour_dict)
        self.assertIn('quantity', flour_dict)
        self.assertIn('supplier', flour_dict)
        
        # Check the values
        self.assertEqual(flour_dict['name'], 'Flour')
        self.assertEqual(flour_dict['calories'], 100)
    
    # Case 4: Test ingredient.values_list()
    def test_queryset_values_list(self):
        """
        Test that .values_list() returns tuples instead of dictionaries.
        Each item is a tuple of field values in the order they're defined.
        """
        # Get all ingredients as tuples
        ingredients = Ingredient.objects.all().values_list()
        
        # Check that we get a QuerySet
        self.assertEqual(type(ingredients).__name__, 'QuerySet')
        
        # Get the first result
        first_ingredient = ingredients.first()
        
        # Check that it's a tuple
        self.assertIsInstance(first_ingredient, tuple)
        
        # Check that it has 7 elements (id + 6 fields)
        self.assertEqual(len(first_ingredient), 7)
        
        # Test values_list with specific fields
        names_only = Ingredient.objects.all().values_list('name', flat=True)
        
        # Should return a flat list of names
        self.assertIn('Flour', names_only)
        self.assertIn('Sugar', names_only)
        self.assertIn('Chocolate Chips', names_only)
        
        # Test values_list with multiple specific fields
        name_price = Ingredient.objects.filter(name='Flour').values_list('name', 'price')
        self.assertEqual(name_price.first(), ('Flour', 2.50))
    
    # Case 5: Test Ingredient.objects.get(id=1)
    def test_queryset_get_by_id(self):
        """
        Test that .get() returns a single model instance (not a QuerySet).
        .get() raises DoesNotExist if no match, or MultipleObjectsReturned if multiple matches.
        """
        # Get the flour ingredient by its ID
        ingredient = Ingredient.objects.get(id=self.flour.id)
        
        # Check that it's an Ingredient instance (not a QuerySet)
        self.assertIsInstance(ingredient, Ingredient)
        
        # Check that it's the correct ingredient
        self.assertEqual(ingredient, self.flour)
        self.assertEqual(ingredient.name, 'Flour')
        
        # Test that .get() raises DoesNotExist for non-existent ID
        with self.assertRaises(Ingredient.DoesNotExist):
            Ingredient.objects.get(id=99999)
        
        # Test .get() with other fields
        sugar = Ingredient.objects.get(name='Sugar')
        self.assertEqual(sugar, self.sugar)
        