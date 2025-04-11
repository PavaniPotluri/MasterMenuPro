import json
from flask import render_template, request, redirect, url_for, session, jsonify, flash
from app import app, db
from models import MealPlan, MealPlanDay
from meal_planner import generate_meal_plan, get_recipe_details
from usda_guidelines import get_calorie_target, get_macronutrient_targets
import logging

@app.route('/')
def index():
    """Render the home page with meal preference form"""
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    """Generate a meal plan based on user preferences"""
    try:
        # Get user preferences from form
        preferences = {
            'calorie_target': int(request.form.get('calorie_target', 2000)),
            'diet_type': request.form.get('diet_type', 'balanced'),
            'vegetarian': 'vegetarian' in request.form,
            'vegan': 'vegan' in request.form,
            'gluten_free': 'gluten_free' in request.form,
            'dairy_free': 'dairy_free' in request.form,
            'allergens': request.form.get('allergens', '')
        }
        
        # Store preferences in session
        session['preferences'] = preferences
        
        # Generate meal plan
        meal_plan = generate_meal_plan(preferences)
        
        # Store meal plan in database (for anonymous user)
        db_meal_plan = MealPlan(name="Weekly Meal Plan")
        db.session.add(db_meal_plan)
        db.session.flush()
        
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, day in enumerate(meal_plan):
            meal_day = MealPlanDay(
                meal_plan_id=db_meal_plan.id,
                day_of_week=i,
                breakfast=day['breakfast'],
                lunch=day['lunch'],
                dinner=day['dinner'],
                snacks=day['snacks'],
                total_calories=day['nutrition']['calories'],
                total_protein=day['nutrition']['protein'],
                total_carbs=day['nutrition']['carbs'],
                total_fat=day['nutrition']['fat'],
                total_fiber=day['nutrition']['fiber']
            )
            db.session.add(meal_day)
        
        db.session.commit()
        
        # Redirect to meal plan view
        return redirect(url_for('view_plan', plan_id=db_meal_plan.id))
    
    except Exception as e:
        logging.error(f"Error generating meal plan: {str(e)}")
        flash(f"Error generating meal plan: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/plan/<int:plan_id>')
def view_plan(plan_id):
    """View a generated meal plan"""
    meal_plan = MealPlan.query.get_or_404(plan_id)
    days = meal_plan.days
    
    # Get USDA guideline targets based on calorie level
    preferences = session.get('preferences', {'calorie_target': 2000})
    calorie_target = preferences['calorie_target']
    macro_targets = get_macronutrient_targets(calorie_target)
    
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    return render_template(
        'meal_plan.html', 
        meal_plan=meal_plan,
        days=days,
        days_of_week=days_of_week,
        preferences=preferences,
        macro_targets=macro_targets
    )

@app.route('/recipe/<recipe_id>')
def recipe_details(recipe_id):
    """View details for a specific recipe"""
    recipe = get_recipe_details(recipe_id)
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/api/guidelines')
def get_guidelines():
    """API endpoint to get USDA guidelines based on calorie target"""
    calorie_target = request.args.get('calories', 2000, type=int)
    macro_targets = get_macronutrient_targets(calorie_target)
    return jsonify(macro_targets)

@app.route('/regenerate_day', methods=['POST'])
def regenerate_day():
    """Regenerate a specific day in the meal plan"""
    try:
        plan_id = request.form.get('plan_id', type=int)
        day_index = request.form.get('day_index', type=int)
        
        meal_plan = MealPlan.query.get_or_404(plan_id)
        day = MealPlanDay.query.filter_by(meal_plan_id=plan_id, day_of_week=day_index).first_or_404()
        
        # Get preferences from session
        preferences = session.get('preferences', {
            'calorie_target': 2000,
            'diet_type': 'balanced',
            'vegetarian': False,
            'vegan': False,
            'gluten_free': False,
            'dairy_free': False,
            'allergens': ''
        })
        
        # Generate a new day's meal plan
        new_day = generate_meal_plan(preferences, days=1)[0]
        
        # Update the day in the database
        day.breakfast = new_day['breakfast']
        day.lunch = new_day['lunch']
        day.dinner = new_day['dinner']
        day.snacks = new_day['snacks']
        day.total_calories = new_day['nutrition']['calories']
        day.total_protein = new_day['nutrition']['protein']
        day.total_carbs = new_day['nutrition']['carbs']
        day.total_fat = new_day['nutrition']['fat']
        day.total_fiber = new_day['nutrition']['fiber']
        
        db.session.commit()
        
        flash(f"Day {day_index + 1} has been regenerated successfully!", "success")
        return redirect(url_for('view_plan', plan_id=plan_id))
    
    except Exception as e:
        logging.error(f"Error regenerating day: {str(e)}")
        flash(f"Error regenerating day: {str(e)}", "danger")
        return redirect(url_for('view_plan', plan_id=plan_id))
