/**
 * Chart utilities for displaying nutritional information
 */

// Function to create a nutrition bar chart
function createNutritionBarChart(chartId, dayData, targetData) {
  const ctx = document.getElementById(chartId).getContext('2d');
  
  // Calculate percentage of targets
  const proteinPercentage = (dayData.protein / targetData.protein.grams) * 100;
  const carbsPercentage = (dayData.carbs / targetData.carbs.grams) * 100;
  const fatPercentage = (dayData.fat / targetData.fat.grams) * 100;
  const fiberPercentage = (dayData.fiber / targetData.fiber.grams) * 100;
  
  // Create chart data
  const data = {
    labels: ['Protein', 'Carbs', 'Fat', 'Fiber'],
    datasets: [
      {
        label: 'Actual (g)',
        data: [
          Math.round(dayData.protein), 
          Math.round(dayData.carbs), 
          Math.round(dayData.fat), 
          Math.round(dayData.fiber)
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      },
      {
        label: 'Target (g)',
        data: [
          targetData.protein.grams, 
          targetData.carbs.grams, 
          targetData.fat.grams, 
          targetData.fiber.grams
        ],
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1
      }
    ]
  };
  
  // Chart configuration
  const config = {
    type: 'bar',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const index = context.dataIndex;
              const label = context.label;
              if (context.datasetIndex === 0) {
                if (label === 'Protein') {
                  return `${Math.round(proteinPercentage)}% of target`;
                } else if (label === 'Carbs') {
                  return `${Math.round(carbsPercentage)}% of target`;
                } else if (label === 'Fat') {
                  return `${Math.round(fatPercentage)}% of target`;
                } else if (label === 'Fiber') {
                  return `${Math.round(fiberPercentage)}% of target`;
                }
              }
              return '';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Grams'
          }
        }
      }
    }
  };
  
  // Create chart
  return new Chart(ctx, config);
}

// Function to create a calorie pie chart
function createCaloriePieChart(chartId, dayData) {
  const ctx = document.getElementById(chartId).getContext('2d');
  
  // Calculate calories from each macronutrient
  const proteinCalories = dayData.protein * 4; // 4 calories per gram
  const carbsCalories = dayData.carbs * 4;     // 4 calories per gram
  const fatCalories = dayData.fat * 9;         // 9 calories per gram
  
  // Create chart data
  const data = {
    labels: ['Protein', 'Carbs', 'Fat'],
    datasets: [
      {
        data: [proteinCalories, carbsCalories, fatCalories],
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }
    ]
  };
  
  // Calculate percentage of total calories
  const totalCalories = proteinCalories + carbsCalories + fatCalories;
  const proteinPercent = Math.round((proteinCalories / totalCalories) * 100);
  const carbsPercent = Math.round((carbsCalories / totalCalories) * 100);
  const fatPercent = Math.round((fatCalories / totalCalories) * 100);
  
  // Chart configuration
  const config = {
    type: 'pie',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label;
              const value = context.raw;
              const percent = context.parsed;
              if (label === 'Protein') {
                return `Protein: ${Math.round(value)} calories (${proteinPercent}%)`;
              } else if (label === 'Carbs') {
                return `Carbs: ${Math.round(value)} calories (${carbsPercent}%)`;
              } else if (label === 'Fat') {
                return `Fat: ${Math.round(value)} calories (${fatPercent}%)`;
              }
              return '';
            }
          }
        }
      }
    }
  };
  
  // Create chart
  return new Chart(ctx, config);
}

// Function to create weekly nutrition summary chart
function createWeeklyNutritionChart(chartId, weekData, targetData) {
  const ctx = document.getElementById(chartId).getContext('2d');
  
  const labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].slice(0, weekData.length);
  
  // Extract data from each day
  const caloriesData = weekData.map(day => day.calories);
  const proteinData = weekData.map(day => day.protein);
  const carbsData = weekData.map(day => day.carbs);
  const fatData = weekData.map(day => day.fat);
  
  // Create chart data
  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Calories',
        data: caloriesData,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        tension: 0.1,
        yAxisID: 'y'
      },
      {
        label: 'Protein (g)',
        data: proteinData,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        tension: 0.1,
        yAxisID: 'y1'
      },
      {
        label: 'Carbs (g)',
        data: carbsData,
        backgroundColor: 'rgba(255, 206, 86, 0.2)',
        borderColor: 'rgba(255, 206, 86, 1)',
        borderWidth: 2,
        tension: 0.1,
        yAxisID: 'y1'
      },
      {
        label: 'Fat (g)',
        data: fatData,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        tension: 0.1,
        yAxisID: 'y1'
      }
    ]
  };
  
  // Chart configuration
  const config = {
    type: 'line',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      stacked: false,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Calories'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Grams'
          },
          grid: {
            drawOnChartArea: false,
          }
        }
      }
    }
  };
  
  // Create chart
  return new Chart(ctx, config);
}
