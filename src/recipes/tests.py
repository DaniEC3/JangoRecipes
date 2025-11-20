from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe


# ============================================
# STEP 1: MODEL TESTS
# ============================================
# These tests verify that your Recipe model works correctly
# They test: creation, fields, relationships, and string representation

class RecipeModelTest(TestCase):
    """
    Test suite for the Recipe model.
    setUpTestData runs once for the entire test class (faster).
    setUp runs before each individual test method (use for data that gets modified).
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        This runs once before all test methods in this class.
        """
        # Create a test user (required for Recipe's ForeignKey)
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test recipe
        cls.recipe = Recipe.objects.create(
            name="Chocolate Cake",
            user=cls.test_user,
            cooking_time=45,
            description="A delicious chocolate cake recipe.",
            ingredients="Flour, Sugar, Cocoa, Eggs, Butter",
            difficulty="Medium",
            instructions="Step 1: Mix dry ingredients. Step 2: Add wet ingredients. Step 3: Bake at 350°F."
        )
    
    # TEST 1: Object Creation
    def test_recipe_creation(self):
        """
        Test that a recipe can be created with all required fields.
        This verifies the object exists and has the correct field values.
        """
        self.assertIsInstance(self.recipe, Recipe)
        self.assertEqual(self.recipe.name, "Chocolate Cake")
        self.assertEqual(self.recipe.user, self.test_user)
        self.assertEqual(self.recipe.cooking_time, 45)
    
    # TEST 2: String Representation
    def test_recipe_str_method(self):
        """
        Test the __str__() method returns the recipe name.
        This is what appears in the Django admin and when you print the object.
        """
        self.assertEqual(str(self.recipe), "Chocolate Cake")
    
    # TEST 3: Field Max Length
    def test_name_max_length(self):
        """
        Test that the name field has the correct max_length.
        This ensures your model definition is correct.
        """
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
     
    # TEST 4: Foreign Key Relationship
    def test_user_relationship(self):
        """
        Test that the recipe is correctly linked to a user.
        This verifies the ForeignKey relationship works.
        """
        self.assertEqual(self.recipe.user.username, 'testuser')
        # Test reverse relationship: user can access their recipes
        user_recipes = self.test_user.recipe_set.all()
        self.assertIn(self.recipe, user_recipes)
    
    # TEST 5: Multiple Recipes per User
    def test_user_can_have_multiple_recipes(self):
        """
        Test that a user can have multiple recipes.
        This verifies the one-to-many relationship.
        """
        # Create a second recipe for the same user
        recipe2 = Recipe.objects.create(
            name="Vanilla Cookies",
            user=self.test_user,
            cooking_time=20,
            description="Simple vanilla cookies.",
            ingredients="Flour, Sugar, Butter, Vanilla",
            difficulty="Easy",
            instructions="Mix and bake."
        )
        
        user_recipes = self.test_user.recipe_set.all()
        self.assertEqual(user_recipes.count(), 2)
        self.assertIn(self.recipe, user_recipes)
        self.assertIn(recipe2, user_recipes)
    
    # TEST 6: Recipe Deletion When User is Deleted
    def test_recipe_deleted_when_user_deleted(self):
        """
        Test CASCADE deletion: when a user is deleted, their recipes are too.
        This verifies the on_delete=CASCADE behavior.
        """
        # Create a new user and recipe for this test
        temp_user = User.objects.create_user(username='tempuser', password='temp123')
        temp_recipe = Recipe.objects.create(
            name="Temp Recipe",
            user=temp_user,
            cooking_time=5,
            description="Temporary",
            ingredients="Test",
            difficulty="Easy",
            instructions="Test"
        )
        
        recipe_id = temp_recipe.id
        
        # Delete the user
        temp_user.delete()
        
        # Verify the recipe was also deleted
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)
    
    # TEST 7: Difficulty Choices
    def test_difficulty_choices(self):
        """
        Test that difficulty field only accepts valid choices
        """
        # Valid choice should work
        recipe = Recipe.objects.create(
            name="Test Recipe",
            user=self.test_user,
            cooking_time=30,
            description="Test",
            ingredients="Test ingredients",
            difficulty="Medium",
            instructions="Test"
        )
        self.assertEqual(recipe.difficulty, "Medium")
        
        # Test default value
        recipe2 = Recipe.objects.create(
            name="Default Recipe",
            user=self.test_user,
            cooking_time=15,
            description="Test",
            ingredients="Test",
            instructions="Test"
        )
        self.assertEqual(recipe2.difficulty, "Easy")  # Should default to Easy