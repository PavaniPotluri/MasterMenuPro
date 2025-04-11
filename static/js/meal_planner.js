/**
 * Meal Planner JavaScript
 * Handles client-side functionality for the meal planner application
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Handle form submission
  const mealPlanForm = document.getElementById('meal-plan-form');
  if (mealPlanForm) {
    mealPlanForm.addEventListener('submit', function(e) {
      const calorieTarget = document.getElementById('calorie-target').value;
      if (!calorieTarget || isNaN(parseInt(calorieTarget))) {
        e.preventDefault();
        alert('Please enter a valid calorie target');
        return false;
      }
      
      // Show loading spinner
      document.getElementById('loading-spinner').classList.remove('d-none');
      return true;
    });
  }
  
  // Initialize nutrition charts if on meal plan page
  const nutritionCharts = document.querySelectorAll('.nutrition-chart');
  if (nutritionCharts.length > 0) {
    initializeNutritionCharts();
  }
  
  // Handle tab switching for meal plan days
  const dayTabs = document.querySelectorAll('[data-bs-toggle="tab"]');
  if (dayTabs.length > 0) {
    dayTabs.forEach(tab => {
      tab.addEventListener('shown.bs.tab', function(event) {
        const targetId = event.target.getAttribute('data-bs-target');
        const dayIndex = targetId.replace('#day-', '');
        updateActiveDay(dayIndex);
      });
    });
  }
  
  // Handle print button
  const printButton = document.getElementById('print-meal-plan');
  if (printButton) {
    printButton.addEventListener('click', function() {
      window.print();
    });
  }
});

// Update active day and refresh charts
function updateActiveDay(dayIndex) {
  // Update URL hash for bookmarking
  window.location.hash = `day-${dayIndex}`;
  
  // Refresh any charts in the active tab
  const chartCanvas = document.querySelector(`#day-${dayIndex} .nutrition-chart`);
  if (chartCanvas && window.dayCharts && window.dayCharts[dayIndex]) {
    window.dayCharts[dayIndex].update();
  }
  
  const pieChartCanvas = document.querySelector(`#day-${dayIndex} .calorie-chart`);
  if (pieChartCanvas && window.pieCharts && window.pieCharts[dayIndex]) {
    window.pieCharts[dayIndex].update();
  }
}

// Initialize all nutrition charts
function initializeNutritionCharts() {
  // Get data from page
  const nutritionData = JSON.parse(document.getElementById('nutrition-data').textContent);
  const targetData = JSON.parse(document.getElementById('target-data').textContent);
  
  // Store chart references for updating later
  window.dayCharts = {};
  window.pieCharts = {};
  
  // Create charts for each day
  for (let i = 0; i < nutritionData.length; i++) {
    const barChartId = `nutrition-chart-${i}`;
    const pieChartId = `calorie-chart-${i}`;
    
    const barChartElement = document.getElementById(barChartId);
    const pieChartElement = document.getElementById(pieChartId);
    
    if (barChartElement) {
      window.dayCharts[i] = createNutritionBarChart(barChartId, nutritionData[i], targetData);
    }
    
    if (pieChartElement) {
      window.pieCharts[i] = createCaloriePieChart(pieChartId, nutritionData[i]);
    }
  }
  
  // Create weekly summary chart if available
  const weeklyChartElement = document.getElementById('weekly-nutrition-chart');
  if (weeklyChartElement) {
    window.weeklyChart = createWeeklyNutritionChart('weekly-nutrition-chart', nutritionData, targetData);
  }
}

// Function to toggle recipe details
function toggleRecipeDetails(recipeId) {
  const detailsElement = document.getElementById(`recipe-details-${recipeId}`);
  if (detailsElement) {
    if (detailsElement.classList.contains('d-none')) {
      detailsElement.classList.remove('d-none');
    } else {
      detailsElement.classList.add('d-none');
    }
  }
}

// Function to handle regenerating a day
function confirmRegenerate(formId) {
  if (confirm('Are you sure you want to regenerate this day\'s meal plan?')) {
    document.getElementById(formId).submit();
  }
}

// Function to save meal plan as PDF (using browser print)
function printMealPlan() {
  window.print();
}

// Function to handle dynamic calorie adjustment
function updateCalorieBreakdown() {
  const calorieTarget = parseInt(document.getElementById('calorie-target').value) || 2000;
  
  // Calculate meal breakdown
  const breakfast = Math.round(calorieTarget * 0.25);
  const lunch = Math.round(calorieTarget * 0.30);
  const dinner = Math.round(calorieTarget * 0.35);
  const snacks = Math.round(calorieTarget * 0.10);
  
  // Update display
  document.getElementById('breakfast-calories').textContent = breakfast;
  document.getElementById('lunch-calories').textContent = lunch;
  document.getElementById('dinner-calories').textContent = dinner;
  document.getElementById('snack-calories').textContent = snacks;
  
  // Update targets display
  document.getElementById('protein-target').textContent = Math.round((calorieTarget * 0.225) / 4); // 22.5% of calories, 4 cal/g
  document.getElementById('carbs-target').textContent = Math.round((calorieTarget * 0.55) / 4);  // 55% of calories, 4 cal/g
  document.getElementById('fat-target').textContent = Math.round((calorieTarget * 0.275) / 9);   // 27.5% of calories, 9 cal/g
}
