from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Ingredient
from .forms import RecipeSearchForm


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
            instructions="Step 1: Mix dry ingredients. Step 2: Add wet ingredients. Step 3: Bake at 350°F."
        )
        i1 = Ingredient.objects.create(name="Flour", calories=100, price=1.0, quantity=1, supplier="Store")
        i2 = Ingredient.objects.create(name="Sugar", calories=100, price=1.0, quantity=1, supplier="Store")
        cls.recipe.ingredients.add(i1, i2)
    
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
            instructions="Mix and bake."
        )
        i3 = Ingredient.objects.create(name="Vanilla", calories=50, price=2.0, quantity=1, supplier="Store")
        recipe2.ingredients.add(i3)
        
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
            instructions="Test"
        )
        i4 = Ingredient.objects.create(name="Test", calories=10, price=0.5, quantity=1, supplier="Store")
        temp_recipe.ingredients.add(i4)
        
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
            instructions="Test"
        )
        i5 = Ingredient.objects.create(name="Test Ing", calories=10, price=0.5, quantity=1, supplier="Store")
        recipe.ingredients.add(i5)
        self.assertEqual(recipe.difficulty, "Intermediate")
    # TEST 8: Absolute URL
    def test_absolute_url(self):
        """
        Test that the absolute URL returns the correct URL for a recipe.
        This verifies the get_absolute_url method works as expected.
        """
        recipe = Recipe.objects.create(
            name="Test Recipe",
            user=self.test_user,
            cooking_time=30,
            description="Test",
            instructions="Test"
        )
        i6 = Ingredient.objects.create(name="Test Ing 2", calories=10, price=0.5, quantity=1, supplier="Store")
        recipe.ingredients.add(i6)
        self.assertEqual(recipe.get_absolute_url(), '/recipe/2')


# ============================================
# RECIPE SEARCH FORM TESTS
# ============================================

class RecipeSearchFormTest(TestCase):
    
    def test_form_valid(self):
        """Test that a form with valid data is valid"""
        form = RecipeSearchForm(data={'recipe_name': 'test', 'chart_type': '#1'})
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_missing_recipe(self):
        """Test that a form with empty recipe_name is invalid"""
        form = RecipeSearchForm(data={'recipe_name': '', 'chart_type': '#1'})
        self.assertFalse(form.is_valid())
        self.assertIn('recipe_name', form.errors)
    
    def test_form_invalid_missing_chart_type(self):
        """Test that a form without chart_type is invalid"""
        form = RecipeSearchForm(data={'recipe_name': 'test'})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)
    
    def test_chart_form_invalid_choice(self):
        """Test that a form with invalid chart_type is invalid"""
        form = RecipeSearchForm(data={'recipe_name': 'test', 'chart_type': 'invalid'})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)


# ============================================
# INGREDIENT MODEL TESTS
# ============================================

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


# ============================================
# USER AUTHENTICATION TESTS
# ============================================

class LoginViewTest(TestCase):
    """
    Test suite for the login view.
    Tests GET requests, POST with valid/invalid credentials, and redirects.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Create a test user for authentication tests.
        This runs once before all tests in this class.
        """
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.login_url = '/login/'
    
    def test_login_view_get_request(self):
        """
        Test that GET request to login page returns 200 and uses correct template.
        """
        response = self.client.get(self.login_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertIn('form', response.context)
        self.assertIsNone(response.context.get('error_message'))
    
    def test_login_view_post_valid_credentials(self):
        """
        Test that POST with valid credentials logs user in and redirects to home.
        """
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should redirect to recipes home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/recipe/home/')
        
        # Verify user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'testuser')
    
    def test_login_view_post_invalid_username(self):
        """
        Test that POST with invalid username shows error message.
        """
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'testpass123'
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        
        # Should show error message
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], 'Invalid username or password')
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_invalid_password(self):
        """
        Test that POST with invalid password shows error message.
        """
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        
        # Should show error message
        self.assertEqual(response.context['error_message'], 'Invalid username or password')
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_empty_credentials(self):
        """
        Test that POST with empty credentials shows form errors.
        """
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        
        # Form should have errors
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    """
    Test suite for the logout view.
    Tests that users can successfully log out and are redirected properly.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Create a test user for logout tests.
        """
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.logout_url = '/logout/'
    
    def test_logout_view_redirects_to_login(self):
        """
        Test that logout redirects to login page.
        """
        # First log in the user
        self.client.login(username='testuser', password='testpass123')
        
        # Then log out
        response = self.client.get(self.logout_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
    
    def test_logout_view_logs_user_out(self):
        """
        Test that logout actually logs the user out.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpass123')
        
        # Verify user is logged in
        response = self.client.get('/recipe/home/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Log out
        self.client.get(self.logout_url)
        
        # Verify user is logged out
        response = self.client.get('/login/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegisterViewTest(TestCase):
    """
    Test suite for the registration view.
    Tests user registration with valid/invalid data, password validation, and username uniqueness.
    """
    
    def setUp(self):
        """
        Set up runs before each test method.
        No pre-existing users needed for most registration tests.
        """
        self.register_url = '/register/'
    
    def test_register_view_get_request(self):
        """
        Test that GET request to register page returns 200 and uses correct template.
        """
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertIn('form', response.context)
        self.assertIsNone(response.context.get('error_message'))
    
    def test_register_view_post_valid_data(self):
        """
        Test that POST with valid data creates user, logs them in, and redirects to home.
        """
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        
        # Should redirect to recipes home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/recipe/home/')
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verify user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'newuser')
    
    def test_register_view_post_password_mismatch(self):
        """
        Test that POST with mismatched passwords shows error.
        """
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'TestPass123!',
            'password2': 'DifferentPass123!'
        })
        
        # Should stay on register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        
        # Should show error message
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], 'Registration failed. Please correct the errors below.')
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_register_view_post_duplicate_username(self):
        """
        Test that POST with existing username shows error.
        """
        # Create an existing user
        User.objects.create_user(username='existinguser', password='TestPass123!')
        
        # Try to register with same username
        response = self.client.post(self.register_url, {
            'username': 'existinguser',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        
        # Should stay on register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        
        # Should show error message
        self.assertEqual(response.context['error_message'], 'Registration failed. Please correct the errors below.')
        
        # Form should have errors
        self.assertFalse(response.context['form'].is_valid())
        
        # Should still be only one user with that username
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)
    
    def test_register_view_post_weak_password(self):
        """
        Test that POST with weak password (too short or common) shows error.
        """
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'pass',
            'password2': 'pass'
        })
        
        # Should stay on register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        
        # Should show error message
        self.assertEqual(response.context['error_message'], 'Registration failed. Please correct the errors below.')
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_register_view_post_empty_fields(self):
        """
        Test that POST with empty fields shows form errors.
        """
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': '',
            'password2': ''
        })
        
        # Should stay on register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        
        # Form should have errors
        self.assertFalse(response.context['form'].is_valid())
        
        # User should not be created
        self.assertEqual(User.objects.count(), 0)
    
    def test_register_view_post_numeric_password(self):
        """
        Test that POST with purely numeric password shows error.
        Django's default validators reject purely numeric passwords.
        """
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': '12345678',
            'password2': '12345678'
        })
        
        # Should stay on register page
        self.assertEqual(response.status_code, 200)
        
        # Should show error message
        self.assertEqual(response.context['error_message'], 'Registration failed. Please correct the errors below.')
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())
        