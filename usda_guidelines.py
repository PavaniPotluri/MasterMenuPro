"""
USDA Dietary Guidelines Implementation

This module contains functionality related to USDA dietary guidelines, including:
- Calorie target calculations
- Macronutrient distribution recommendations
- Daily nutrition targets
"""

# USDA calorie levels based on age, gender, and activity level
CALORIE_LEVELS = {
    'sedentary': {
        'male': {
            '2-3': 1000,
            '4-8': 1200,
            '9-13': 1600,
            '14-18': 2000,
            '19-30': 2400,
            '31-50': 2200,
            '51+': 2000
        },
        'female': {
            '2-3': 1000,
            '4-8': 1200,
            '9-13': 1400,
            '14-18': 1800,
            '19-30': 1800,
            '31-50': 1800,
            '51+': 1600
        }
    },
    'moderately_active': {
        'male': {
            '2-3': 1000,
            '4-8': 1400,
            '9-13': 1800,
            '14-18': 2400,
            '19-30': 2600,
            '31-50': 2400,
            '51+': 2200
        },
        'female': {
            '2-3': 1000,
            '4-8': 1400,
            '9-13': 1600,
            '14-18': 2000,
            '19-30': 2000,
            '31-50': 2000,
            '51+': 1800
        }
    },
    'active': {
        'male': {
            '2-3': 1000,
            '4-8': 1600,
            '9-13': 2000,
            '14-18': 2800,
            '19-30': 3000,
            '31-50': 2800,
            '51+': 2400
        },
        'female': {
            '2-3': 1000,
            '4-8': 1400,
            '9-13': 1800,
            '14-18': 2400,
            '19-30': 2400,
            '31-50': 2200,
            '51+': 2000
        }
    }
}

# Macronutrient distribution ranges
# Values are in percentages of total calories
MACRONUTRIENT_RANGES = {
    'protein': (10, 35),  # 10-35% of calories from protein
    'carbs': (45, 65),    # 45-65% of calories from carbohydrates
    'fat': (20, 35)       # 20-35% of calories from fat
}

# Recommended fiber intake by calorie level
FIBER_RECOMMENDATIONS = {
    1000: 19,
    1200: 21,
    1400: 23,
    1600: 25,
    1800: 25,
    2000: 28,
    2200: 30,
    2400: 31,
    2600: 33,
    2800: 34,
    3000: 35
}

def get_calorie_target(age, gender, activity_level):
    """
    Calculate calorie target based on age, gender, and activity level
    """
    # Determine age group
    if 2 <= age <= 3:
        age_group = '2-3'
    elif 4 <= age <= 8:
        age_group = '4-8'
    elif 9 <= age <= 13:
        age_group = '9-13'
    elif 14 <= age <= 18:
        age_group = '14-18'
    elif 19 <= age <= 30:
        age_group = '19-30'
    elif 31 <= age <= 50:
        age_group = '31-50'
    else:
        age_group = '51+'
    
    # Get calorie level
    activity_key = 'sedentary'
    if activity_level == 'moderate':
        activity_key = 'moderately_active'
    elif activity_level == 'active':
        activity_key = 'active'
    
    return CALORIE_LEVELS[activity_key][gender][age_group]

def get_macronutrient_targets(calorie_target):
    """
    Calculate macronutrient targets based on calorie target
    Returns targets in grams for protein, carbs, and fat
    """
    # Calculate average percentages within the AMDR (Acceptable Macronutrient Distribution Range)
    protein_percent = (MACRONUTRIENT_RANGES['protein'][0] + MACRONUTRIENT_RANGES['protein'][1]) / 2
    carbs_percent = (MACRONUTRIENT_RANGES['carbs'][0] + MACRONUTRIENT_RANGES['carbs'][1]) / 2
    fat_percent = (MACRONUTRIENT_RANGES['fat'][0] + MACRONUTRIENT_RANGES['fat'][1]) / 2
    
    # Calculate grams of each macronutrient
    # 4 calories per gram of protein
    protein_grams = (calorie_target * (protein_percent / 100)) / 4
    # 4 calories per gram of carbohydrate
    carbs_grams = (calorie_target * (carbs_percent / 100)) / 4
    # 9 calories per gram of fat
    fat_grams = (calorie_target * (fat_percent / 100)) / 9
    
    # Find nearest fiber recommendation
    fiber_recommendation = 0
    closest_calorie = min(FIBER_RECOMMENDATIONS.keys(), key=lambda x: abs(x - calorie_target))
    fiber_recommendation = FIBER_RECOMMENDATIONS[closest_calorie]
    
    # Calculate recommended ranges
    protein_range = [
        (calorie_target * (MACRONUTRIENT_RANGES['protein'][0] / 100)) / 4,
        (calorie_target * (MACRONUTRIENT_RANGES['protein'][1] / 100)) / 4
    ]
    
    carbs_range = [
        (calorie_target * (MACRONUTRIENT_RANGES['carbs'][0] / 100)) / 4,
        (calorie_target * (MACRONUTRIENT_RANGES['carbs'][1] / 100)) / 4
    ]
    
    fat_range = [
        (calorie_target * (MACRONUTRIENT_RANGES['fat'][0] / 100)) / 9,
        (calorie_target * (MACRONUTRIENT_RANGES['fat'][1] / 100)) / 9
    ]
    
    return {
        'calories': calorie_target,
        'protein': {
            'grams': round(protein_grams),
            'range': [round(protein_range[0]), round(protein_range[1])],
            'percent': protein_percent
        },
        'carbs': {
            'grams': round(carbs_grams),
            'range': [round(carbs_range[0]), round(carbs_range[1])],
            'percent': carbs_percent
        },
        'fat': {
            'grams': round(fat_grams),
            'range': [round(fat_range[0]), round(fat_range[1])],
            'percent': fat_percent
        },
        'fiber': {
            'grams': fiber_recommendation
        }
    }

def get_meal_breakdown(calorie_target):
    """
    Provide a breakdown of how calories should be distributed across meals
    """
    return {
        'breakfast': int(calorie_target * 0.25),
        'lunch': int(calorie_target * 0.30),
        'dinner': int(calorie_target * 0.35),
        'snacks': int(calorie_target * 0.10)
    }

def check_nutrient_compliance(meal_plan, calorie_target):
    """
    Check if a meal plan meets USDA guidelines
    Returns compliance percentages and recommendations
    """
    targets = get_macronutrient_targets(calorie_target)
    
    # Calculate average daily nutrition values
    total_days = len(meal_plan)
    avg_calories = sum(day['nutrition']['calories'] for day in meal_plan) / total_days
    avg_protein = sum(day['nutrition']['protein'] for day in meal_plan) / total_days
    avg_carbs = sum(day['nutrition']['carbs'] for day in meal_plan) / total_days
    avg_fat = sum(day['nutrition']['fat'] for day in meal_plan) / total_days
    avg_fiber = sum(day['nutrition']['fiber'] for day in meal_plan) / total_days
    
    # Calculate compliance percentages
    calorie_compliance = (avg_calories / calorie_target) * 100
    protein_compliance = (avg_protein / targets['protein']['grams']) * 100
    carbs_compliance = (avg_carbs / targets['carbs']['grams']) * 100
    fat_compliance = (avg_fat / targets['fat']['grams']) * 100
    fiber_compliance = (avg_fiber / targets['fiber']['grams']) * 100
    
    # Generate recommendations
    recommendations = []
    
    if calorie_compliance < 90:
        recommendations.append("Increase overall calorie intake")
    elif calorie_compliance > 110:
        recommendations.append("Reduce overall calorie intake")
    
    if protein_compliance < 90:
        recommendations.append("Increase protein intake")
    elif protein_compliance > 110:
        recommendations.append("Consider reducing protein slightly")
    
    if carbs_compliance < 90:
        recommendations.append("Increase carbohydrate intake")
    elif carbs_compliance > 110:
        recommendations.append("Reduce carbohydrate intake")
    
    if fat_compliance < 90:
        recommendations.append("Increase healthy fat intake")
    elif fat_compliance > 110:
        recommendations.append("Reduce fat intake")
    
    if fiber_compliance < 90:
        recommendations.append("Increase fiber intake by adding more fruits, vegetables, and whole grains")
    
    return {
        'compliance': {
            'calories': round(calorie_compliance),
            'protein': round(protein_compliance),
            'carbs': round(carbs_compliance),
            'fat': round(fat_compliance),
            'fiber': round(fiber_compliance)
        },
        'recommendations': recommendations
    }
