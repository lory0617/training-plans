function calculateBMI(weight, height) {
  const h = height / 100; // convert cm to m
  return weight / (h * h);
}

function calculateBMR(weight, height, age, gender) {
  if (gender === 'male') {
    return 10 * weight + 6.25 * height - 5 * age + 5;
  }
  return 10 * weight + 6.25 * height - 5 * age - 161;
}

function estimateCalories(bmr, activity = 1.55) {
  return bmr * activity;
}
