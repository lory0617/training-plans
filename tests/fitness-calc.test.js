const assert = require('assert');
const { calculateBMI, calculateBMR, estimateCalories } = require('../fitness-calc.js');

function nearlyEqual(actual, expected, delta = 0.001) {
  assert.ok(Math.abs(actual - expected) <= delta,
    `${actual} not within ${delta} of ${expected}`);
}

// Typical input values
const weight = 70;    // kg
const height = 170;   // cm
const age = 30;       // years
const gender = 'male';

const bmiExpected = weight / ((height / 100) ** 2);
const bmi = calculateBMI(weight, height);
nearlyEqual(bmi, bmiExpected);

const bmrExpected = 10 * weight + 6.25 * height - 5 * age + 5;
const bmr = calculateBMR(weight, height, age, gender);
nearlyEqual(bmr, bmrExpected);

const caloriesExpected = bmrExpected * 1.55;
const calories = estimateCalories(bmr, 1.55);
nearlyEqual(calories, caloriesExpected);

console.log('All tests passed!');
