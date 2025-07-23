from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('bmr'):
            bmr = float(request.form['bmr'])
            activity_level = request.form['activity_level']
            experience = request.form['experience']
            goal = request.form['goal']
            weight = float(request.form['weight'])

            tdee = calculate_tdee(bmr, activity_level)
            total_calories = calculate_total_calories(tdee, goal, experience)
            protein_min, protein_max, fat_min, fat_max, carbs = calculate_macronutrients(total_calories, weight, goal)

            tdee = int(tdee)
            total_calories = int(total_calories)
            protein_min = int(protein_min)
            protein_max = int(protein_max)
            fat_min = int(fat_min)
            fat_max = int(fat_max)
            carbs = int(carbs)

            protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content = suggest_foods(
                protein_min, protein_max, fat_min, fat_max, carbs)

            return render_template(
                'result_manual.html',
                bmr=bmr,
                tdee=tdee,
                total_calories=total_calories,
                protein_min=protein_min,
                protein_max=protein_max,
                fat_min=fat_min,
                fat_max=fat_max,
                carbs=carbs,
                protein_foods=protein_foods,
                fat_foods=fat_foods,
                carb_foods=carb_foods,
                protein_content=protein_content,
                fat_content=fat_content,
                carb_content=carb_content,
            )
        else:
            gender = request.form['gender']
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            age = int(request.form['age'])

            bmr = calculate_bmr(gender, height, weight, age)

            activity_level = request.form['activity_level']
            experience = request.form['experience']
            goal = request.form['goal']
            weight = float(request.form['weight'])

            tdee = calculate_tdee(bmr, activity_level)
            total_calories = calculate_total_calories(tdee, goal, experience)
            protein_min, protein_max, fat_min, fat_max, carbs = calculate_macronutrients(total_calories, weight, goal)

            tdee = int(tdee)
            total_calories = int(total_calories)
            protein_min = int(protein_min)
            protein_max = int(protein_max)
            fat_min = int(fat_min)
            fat_max = int(fat_max)
            carbs = int(carbs)

            protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content = suggest_foods(
                protein_min, protein_max, fat_min, fat_max, carbs)

            return render_template(
                'result_manual.html',
                bmr=bmr,
                tdee=tdee,
                total_calories=total_calories,
                protein_min=protein_min,
                protein_max=protein_max,
                fat_min=fat_min,
                fat_max=fat_max,
                carbs=carbs,
                protein_foods=protein_foods,
                fat_foods=fat_foods,
                carb_foods=carb_foods,
                protein_content=protein_content,
                fat_content=fat_content,
                carb_content=carb_content,
            )

    return render_template('index.html')

def calculate_bmr(gender, height, weight, age):
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

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
    if experience == '新手':
        if goal == '增肌':
            total_calories = tdee + 100
        elif goal == '減脂':
            total_calories = tdee - 200
        else:
            raise ValueError('Invalid goal')
    elif experience == '老手':
        if goal == '增肌':
            total_calories = tdee + 300
        elif goal == '減脂':
            total_calories = tdee - 400
        else:
            raise ValueError('Invalid goal')
    else:
        raise ValueError('Invalid experience')
    return total_calories

def calculate_macronutrients(total_calories, weight, goal):
    if goal == '增肌':
        protein_min = weight * 1.6
        protein_max = weight * 2.2
    elif goal == '減脂':
        protein_min = weight * 2.2
        protein_max = weight * 2.5
    else:
        raise ValueError('Invalid goal')

    fat_min = weight * 0.8
    fat_max = weight * 1

    remaining_calories = total_calories - ((protein_min + protein_max) / 2 * 4) - ((fat_min + fat_max) / 2 * 9)
    carbs = remaining_calories / 4

    return protein_min, protein_max, fat_min, fat_max, carbs

def suggest_foods(protein_min, protein_max, fat_min, fat_max, carbs):
    protein_suggestion = (protein_min + protein_max) / 2
    fat_suggestion = (fat_min + fat_max) / 2
    carbs_suggestion = carbs

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

    protein_foods = {
        '雞胸肉': round(protein_suggestion / 30),
        '鮭魚': round(protein_suggestion / 20),
        '牛肉': round(protein_suggestion / 26),
        '乳清蛋白粉': round(protein_suggestion / 23),
    }

    fat_foods = {
        '堅果': round(fat_suggestion / 5.5),
        '橄欖油': round(fat_suggestion / 10),
    }

    carb_foods = {
        '白米': round(carbs_suggestion / 29),
        '燕麥': round(carbs_suggestion / 60),
        '地瓜': round(carbs_suggestion / 23),
        '馬鈴薯': round(carbs_suggestion / 18),
    }

    return protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
