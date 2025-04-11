from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    
    # User preferences
    calorie_target = db.Column(db.Integer, default=2000)
    diet_type = db.Column(db.String(50), default="balanced")  # balanced, low-carb, etc.
    
    # Dietary restrictions
    vegetarian = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    gluten_free = db.Column(db.Boolean, default=False)
    dairy_free = db.Column(db.Boolean, default=False)
    
    # Allergens (stored as comma-separated values)
    allergens = db.Column(db.String(255), default="")
    
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True)

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), default="Weekly Meal Plan")
    
    days = db.relationship('MealPlanDay', backref='meal_plan', lazy=True, cascade='all, delete-orphan')

class MealPlanDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6 for Monday-Sunday
    
    breakfast = db.Column(db.JSON, nullable=True)
    lunch = db.Column(db.JSON, nullable=True)
    dinner = db.Column(db.JSON, nullable=True)
    snacks = db.Column(db.JSON, nullable=True)
    
    total_calories = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    total_carbs = db.Column(db.Float, default=0)
    total_fat = db.Column(db.Float, default=0)
    total_fiber = db.Column(db.Float, default=0)
