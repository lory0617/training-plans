from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        activity_level = request.form['activity_level']
        experience = request.form['experience']
        goal = request.form['goal']
        weight = float(request.form['weight'])

        if request.form.get('bmr'):
            bmr = float(request.form['bmr'])
            bmr_method = '手動輸入'
            lean_mass = None
        else:
            gender = request.form['gender']
            height = float(request.form['height'])
            age = int(request.form['age'])
            body_fat = float(request.form.get('body_fat') or 0)

            if body_fat > 0:
                bmr = calculate_bmr_katch_mcardle(weight, body_fat)
                bmr_method = 'Katch-McArdle'
                lean_mass = round(weight * (1 - body_fat / 100), 1)
            else:
                bmr = calculate_bmr(gender, height, weight, age)
                bmr_method = 'Mifflin-St Jeor'
                lean_mass = None

        tdee = calculate_tdee(bmr, activity_level)
        total_calories, calorie_percent = calculate_total_calories(tdee, goal, experience)
        protein, fat, carbs, protein_per_kg, fat_per_kg = calculate_macronutrients(total_calories, weight, goal)

        protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content = suggest_foods(protein, fat, carbs)

        protein_range = '1.6–2.2' if goal == '增肌' else '2.0–2.8'
        fat_range = '0.8–1.2' if goal == '增肌' else '0.8–1.0'

        return render_template(
            'result_manual.html',
            bmr=round(bmr, 1),
            bmr_method=bmr_method,
            lean_mass=lean_mass,
            tdee=int(tdee),
            total_calories=int(total_calories),
            calorie_percent=calorie_percent,
            experience=experience,
            goal=goal,
            protein=int(protein),
            fat=int(fat),
            carbs=int(carbs),
            protein_per_kg=protein_per_kg,
            fat_per_kg=fat_per_kg,
            protein_range=protein_range,
            fat_range=fat_range,
            protein_foods=protein_foods,
            fat_foods=fat_foods,
            carb_foods=carb_foods,
            protein_content=protein_content,
            fat_content=fat_content,
            carb_content=carb_content,
        )

    return render_template('index.html')

def calculate_bmr(gender, height, weight, age):
    """Mifflin-St Jeor (1990) — most accurate for general population."""
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_bmr_katch_mcardle(weight, body_fat_percent):
    """Katch-McArdle — more accurate when body fat % is known."""
    lean_mass = weight * (1 - body_fat_percent / 100)
    return 370 + 21.6 * lean_mass

def calculate_tdee(bmr, activity_level):
    factors = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extremely active': 1.9,
    }
    if activity_level not in factors:
        raise ValueError('Invalid activity level')
    return bmr * factors[activity_level]

def calculate_total_calories(tdee, goal, experience):
    """TDEE percentage-based adjustment."""
    multipliers = {
        ('新手', '增肌'): 1.15,   # +15%
        ('老手', '增肌'): 1.10,   # +10%
        ('新手', '減脂'): 0.80,   # -20%
        ('老手', '減脂'): 0.85,   # -15%
    }
    key = (experience, goal)
    if key not in multipliers:
        raise ValueError('Invalid goal or experience')
    multiplier = multipliers[key]
    total = round(tdee * multiplier)
    percent = round((multiplier - 1) * 100)
    return total, percent

def calculate_macronutrients(total_calories, weight, goal):
    """Protein & fat by g/kg body weight (ISSN position stand)."""
    if goal == '增肌':
        protein_per_kg = 1.8   # range 1.6-2.2
        fat_per_kg = 1.0       # range 0.8-1.2
    elif goal == '減脂':
        protein_per_kg = 2.3   # range 2.0-2.8
        fat_per_kg = 0.9       # range 0.8-1.0
    else:
        raise ValueError('Invalid goal')

    protein = round(protein_per_kg * weight)
    fat = round(fat_per_kg * weight)
    remaining = max(0, total_calories - protein * 4 - fat * 9)
    carbs = round(remaining / 4)

    return protein, fat, carbs, protein_per_kg, fat_per_kg

def suggest_foods(protein, fat, carbs):
    protein_content = {
        '雞胸肉': 30,
        '鮭魚': 20,
        '牛肉': 26,
        '乳清蛋白粉': 23,
    }

    fat_content = {
        '堅果': 5,
        '橄欖油': 10,
    }

    carb_content = {
        '白米': 29,
        '燕麥': 60,
        '地瓜': 23,
        '馬鈴薯': 18,
    }

    protein_foods = {food: round(protein / g) for food, g in protein_content.items()}
    fat_foods = {food: round(fat / g) for food, g in fat_content.items()}
    carb_foods = {food: round(carbs / g) for food, g in carb_content.items()}

    return protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
