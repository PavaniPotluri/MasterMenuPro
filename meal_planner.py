import os
import random
import requests
import json
import logging
from usda_guidelines import get_macronutrient_targets

# Use a recipe API for getting meal data
# Using Spoonacular API but you could replace with any recipe API
API_KEY = os.environ.get("SPOONACULAR_API_KEY", "demo-key")
API_BASE_URL = "https://api.spoonacular.com"

# Sample recipes for backup/fallback when API is not available
FALLBACK_RECIPES = {
    "breakfast": [
        {
            "id": 1,
            "title": "Oatmeal with Fruit",
            "image": "https://spoonacular.com/recipeImages/636025-312x231.jpg",
            "readyInMinutes": 10,
            "servings": 1,
            "nutrition": {
                "calories": 250,
                "protein": 8,
                "carbs": 45,
                "fat": 5,
                "fiber": 7
            },
            "sourceUrl": "#"
        },
        {
            "id": 2,
            "title": "Greek Yogurt Parfait",
            "image": "https://spoonacular.com/recipeImages/648506-312x231.jpg",
            "readyInMinutes": 5,
            "servings": 1,
            "nutrition": {
                "calories": 220,
                "protein": 15,
                "carbs": 30,
                "fat": 5,
                "fiber": 4
            },
            "sourceUrl": "#"
        }
    ],
    "lunch": [
        {
            "id": 3,
            "title": "Grilled Chicken Salad",
            "image": "https://spoonacular.com/recipeImages/649503-312x231.jpg",
            "readyInMinutes": 20,
            "servings": 1,
            "nutrition": {
                "calories": 350,
                "protein": 30,
                "carbs": 20,
                "fat": 15,
                "fiber": 5
            },
            "sourceUrl": "#"
        },
        {
            "id": 4,
            "title": "Quinoa Bowl with Vegetables",
            "image": "https://spoonacular.com/recipeImages/641975-312x231.jpg",
            "readyInMinutes": 30,
            "servings": 1,
            "nutrition": {
                "calories": 380,
                "protein": 12,
                "carbs": 60,
                "fat": 10,
                "fiber": 8
            },
            "sourceUrl": "#"
        }
    ],
    "dinner": [
        {
            "id": 5,
            "title": "Baked Salmon with Roasted Vegetables",
            "image": "https://spoonacular.com/recipeImages/640117-312x231.jpg",
            "readyInMinutes": 40,
            "servings": 1,
            "nutrition": {
                "calories": 450,
                "protein": 35,
                "carbs": 25,
                "fat": 20,
                "fiber": 6
            },
            "sourceUrl": "#"
        },
        {
            "id": 6,
            "title": "Vegetable Stir Fry with Tofu",
            "image": "https://spoonacular.com/recipeImages/661925-312x231.jpg",
            "readyInMinutes": 25,
            "servings": 1,
            "nutrition": {
                "calories": 320,
                "protein": 18,
                "carbs": 35,
                "fat": 12,
                "fiber": 8
            },
            "sourceUrl": "#"
        }
    ],
    "snacks": [
        {
            "id": 7,
            "title": "Apple with Almond Butter",
            "image": "https://spoonacular.com/recipeImages/641411-312x231.jpg",
            "readyInMinutes": 2,
            "servings": 1,
            "nutrition": {
                "calories": 180,
                "protein": 5,
                "carbs": 25,
                "fat": 8,
                "fiber": 5
            },
            "sourceUrl": "#"
        },
        {
            "id": 8,
            "title": "Carrot Sticks with Hummus",
            "image": "https://spoonacular.com/recipeImages/641411-312x231.jpg",
            "readyInMinutes": 5,
            "servings": 1,
            "nutrition": {
                "calories": 120,
                "protein": 4,
                "carbs": 15,
                "fat": 6,
                "fiber": 4
            },
            "sourceUrl": "#"
        }
    ]
}

def search_recipes(meal_type, preferences, calories_per_meal):
    """
    Search for recipes based on user preferences and meal type
    """
    try:
        # Build query parameters
        params = {
            "apiKey": API_KEY,
            "number": 5,  # Number of results to return
            "type": meal_type,
            "maxCalories": int(calories_per_meal * 1.1),  # Allow some flexibility
            "minCalories": int(calories_per_meal * 0.9)
        }
        
        # Add dietary restrictions
        if preferences.get('vegetarian'):
            params['vegetarian'] = 'true'
        if preferences.get('vegan'):
            params['vegan'] = 'true'
        if preferences.get('gluten_free'):
            params['glutenFree'] = 'true'
        if preferences.get('dairy_free'):
            params['dairyFree'] = 'true'
        
        # Add diet type
        diet_type = preferences.get('diet_type', 'balanced')
        if diet_type == 'low-carb':
            params['diet'] = 'low-carb'
        elif diet_type == 'high-protein':
            params['diet'] = 'high-protein'
        elif diet_type == 'low-fat':
            params['diet'] = 'low-fat'
        
        # Add allergens to exclude
        if preferences.get('allergens'):
            allergens = preferences['allergens'].split(',')
            params['intolerances'] = ','.join([a.strip() for a in allergens])
        
        # Make API request
        response = requests.get(f"{API_BASE_URL}/recipes/complexSearch", params=params)
        response.raise_for_status()  # Raise exception for non-200 responses
        
        results = response.json()
        
        # Get nutritional information for each recipe
        recipes = []
        for recipe in results.get('results', []):
            recipe_with_nutrition = get_recipe_details(recipe['id'])
            recipes.append(recipe_with_nutrition)
        
        return recipes
    
    except requests.RequestException as e:
        logging.error(f"API request error: {str(e)}")
        # Return fallback recipes if API call fails
        return FALLBACK_RECIPES[meal_type]
    
    except Exception as e:
        logging.error(f"Error searching recipes: {str(e)}")
        return FALLBACK_RECIPES[meal_type]

def get_recipe_details(recipe_id):
    """
    Get detailed information for a specific recipe
    """
    try:
        params = {
            "apiKey": API_KEY,
            "includeNutrition": "true"
        }
        
        response = requests.get(f"{API_BASE_URL}/recipes/{recipe_id}/information", params=params)
        response.raise_for_status()
        
        recipe = response.json()
        
        # Extract essential nutrition information
        nutrition = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }
        
        if 'nutrition' in recipe and 'nutrients' in recipe['nutrition']:
            for nutrient in recipe['nutrition']['nutrients']:
                if nutrient['name'] == 'Calories':
                    nutrition['calories'] = nutrient['amount']
                elif nutrient['name'] == 'Protein':
                    nutrition['protein'] = nutrient['amount']
                elif nutrient['name'] == 'Carbohydrates':
                    nutrition['carbs'] = nutrient['amount']
                elif nutrient['name'] == 'Fat':
                    nutrition['fat'] = nutrient['amount']
                elif nutrient['name'] == 'Fiber':
                    nutrition['fiber'] = nutrient['amount']
        
        # Extract ingredients and instructions
        ingredients = []
        if 'extendedIngredients' in recipe:
            for ingredient in recipe['extendedIngredients']:
                ingredients.append({
                    'name': ingredient.get('name', ''),
                    'amount': ingredient.get('amount', 0),
                    'unit': ingredient.get('unit', '')
                })
        
        instructions = []
        if 'analyzedInstructions' in recipe and recipe['analyzedInstructions']:
            for step in recipe['analyzedInstructions'][0]['steps']:
                instructions.append(step.get('step', ''))
        
        # Format recipe data
        recipe_details = {
            'id': recipe.get('id'),
            'title': recipe.get('title'),
            'image': recipe.get('image'),
            'readyInMinutes': recipe.get('readyInMinutes'),
            'servings': recipe.get('servings'),
            'sourceUrl': recipe.get('sourceUrl'),
            'nutrition': nutrition,
            'ingredients': ingredients,
            'instructions': instructions
        }
        
        return recipe_details
    
    except Exception as e:
        logging.error(f"Error getting recipe details: {str(e)}")
        
        # For demo purposes, return a fallback recipe
        for meal_type in FALLBACK_RECIPES:
            for recipe in FALLBACK_RECIPES[meal_type]:
                if recipe['id'] == recipe_id:
                    return recipe
        
        return {
            'id': recipe_id,
            'title': 'Recipe Not Found',
            'image': '',
            'readyInMinutes': 0,
            'servings': 0,
            'nutrition': {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0},
            'ingredients': [],
            'instructions': [],
            'sourceUrl': '#'
        }

def generate_meal_plan(preferences, days=7):
    """
    Generate a weekly meal plan based on user preferences
    """
    try:
        calorie_target = preferences.get('calorie_target', 2000)
        macro_targets = get_macronutrient_targets(calorie_target)
        
        # Distribute calories across meals
        meal_distribution = {
            'breakfast': 0.25,  # 25% of daily calories
            'lunch': 0.30,      # 30% of daily calories
            'dinner': 0.35,     # 35% of daily calories
            'snacks': 0.10      # 10% of daily calories
        }
        
        meal_calories = {
            'breakfast': int(calorie_target * meal_distribution['breakfast']),
            'lunch': int(calorie_target * meal_distribution['lunch']),
            'dinner': int(calorie_target * meal_distribution['dinner']),
            'snacks': int(calorie_target * meal_distribution['snacks'])
        }
        
        # Generate meal plan for specified number of days
        meal_plan = []
        
        for day in range(days):
            # Get recipes for each meal type
            breakfast_recipes = search_recipes('breakfast', preferences, meal_calories['breakfast'])
            lunch_recipes = search_recipes('lunch', preferences, meal_calories['lunch'])
            dinner_recipes = search_recipes('dinner', preferences, meal_calories['dinner'])
            snack_recipes = search_recipes('snack', preferences, meal_calories['snacks'])
            
            # Select a random recipe for each meal
            breakfast = random.choice(breakfast_recipes) if breakfast_recipes else None
            lunch = random.choice(lunch_recipes) if lunch_recipes else None
            dinner = random.choice(dinner_recipes) if dinner_recipes else None
            snack = random.choice(snack_recipes) if snack_recipes else None
            
            # Calculate day's nutrition totals
            day_nutrition = {
                'calories': (breakfast.get('nutrition', {}).get('calories', 0) if breakfast else 0) +
                            (lunch.get('nutrition', {}).get('calories', 0) if lunch else 0) +
                            (dinner.get('nutrition', {}).get('calories', 0) if dinner else 0) +
                            (snack.get('nutrition', {}).get('calories', 0) if snack else 0),
                            
                'protein': (breakfast.get('nutrition', {}).get('protein', 0) if breakfast else 0) +
                           (lunch.get('nutrition', {}).get('protein', 0) if lunch else 0) +
                           (dinner.get('nutrition', {}).get('protein', 0) if dinner else 0) +
                           (snack.get('nutrition', {}).get('protein', 0) if snack else 0),
                           
                'carbs': (breakfast.get('nutrition', {}).get('carbs', 0) if breakfast else 0) +
                         (lunch.get('nutrition', {}).get('carbs', 0) if lunch else 0) +
                         (dinner.get('nutrition', {}).get('carbs', 0) if dinner else 0) +
                         (snack.get('nutrition', {}).get('carbs', 0) if snack else 0),
                         
                'fat': (breakfast.get('nutrition', {}).get('fat', 0) if breakfast else 0) +
                       (lunch.get('nutrition', {}).get('fat', 0) if lunch else 0) +
                       (dinner.get('nutrition', {}).get('fat', 0) if dinner else 0) +
                       (snack.get('nutrition', {}).get('fat', 0) if snack else 0),
                       
                'fiber': (breakfast.get('nutrition', {}).get('fiber', 0) if breakfast else 0) +
                         (lunch.get('nutrition', {}).get('fiber', 0) if lunch else 0) +
                         (dinner.get('nutrition', {}).get('fiber', 0) if dinner else 0) +
                         (snack.get('nutrition', {}).get('fiber', 0) if snack else 0)
            }
            
            # Add day to meal plan
            meal_plan.append({
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'snacks': snack,
                'nutrition': day_nutrition
            })
        
        return meal_plan
    
    except Exception as e:
        logging.error(f"Error generating meal plan: {str(e)}")
        
        # Generate a basic fallback meal plan if there's an error
        fallback_plan = []
        for day in range(days):
            breakfast = random.choice(FALLBACK_RECIPES['breakfast'])
            lunch = random.choice(FALLBACK_RECIPES['lunch'])
            dinner = random.choice(FALLBACK_RECIPES['dinner'])
            snack = random.choice(FALLBACK_RECIPES['snacks'])
            
            day_nutrition = {
                'calories': breakfast['nutrition']['calories'] + lunch['nutrition']['calories'] + 
                            dinner['nutrition']['calories'] + snack['nutrition']['calories'],
                'protein': breakfast['nutrition']['protein'] + lunch['nutrition']['protein'] + 
                           dinner['nutrition']['protein'] + snack['nutrition']['protein'],
                'carbs': breakfast['nutrition']['carbs'] + lunch['nutrition']['carbs'] + 
                         dinner['nutrition']['carbs'] + snack['nutrition']['carbs'],
                'fat': breakfast['nutrition']['fat'] + lunch['nutrition']['fat'] + 
                       dinner['nutrition']['fat'] + snack['nutrition']['fat'],
                'fiber': breakfast['nutrition']['fiber'] + lunch['nutrition']['fiber'] + 
                         dinner['nutrition']['fiber'] + snack['nutrition']['fiber']
            }
            
            fallback_plan.append({
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'snacks': snack,
                'nutrition': day_nutrition
            })
        
        return fallback_plan
