const assert = require('assert');
const { calculateBMI, calculateBMR, estimateCalories } = require('./fitness-calc');

// BMI should be approximately 24.22
const bmi = calculateBMI(70, 170);
assert(Math.abs(bmi - 24.22) < 0.01, `Expected BMI around 24.22, got ${bmi}`);

// BMR should be positive and around 1617.5 for the given parameters
const bmr = calculateBMR(70, 170, 30, 'male');
assert(bmr > 0, 'BMR should be positive');
assert(Math.abs(bmr - 1617.5) < 1, `Expected BMR around 1617.5, got ${bmr}`);

// Calories estimation
const calories = estimateCalories(1600, 1.55);
assert(Math.abs(calories - 2480) < 0.01, `Expected calories around 2480, got ${calories}`);

console.log('All tests passed.');
