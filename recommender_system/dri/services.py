import math

# -----------------------
# BMI CALCULATION
# -----------------------
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


# -----------------------
# EER CALCULATION
# -----------------------
def calculate_eer(age, sex, weight_kg, height_cm, physical_activity_level):
    height_m = height_cm / 100
    
    if sex.lower() == 'male':
        eer = 662 - (9.53 * age) + physical_activity_level * (15.91 * weight_kg + 539.6 * height_m)
    elif sex.lower() == 'female':
        eer = 354 - (6.91 * age) + physical_activity_level * (9.36 * weight_kg + 726 * height_m)
    else:
        raise ValueError("Sex must be 'male' or 'female'.")
    return eer


# -----------------------
# Macro Targets based on AMDR
# -----------------------
def calculate_macros(eer):
    # Protein (grams)
    protein_min_g = round((0.10 * eer) / 4, 2)
    protein_max_g = round((0.35 * eer) / 4, 2)

    # Fat (grams)
    fat_min_g = round((0.20 * eer) / 9, 2)
    fat_max_g = round((0.35 * eer) / 9, 2)

    # Carbohydrates (grams)
    carb_min_g = round((0.45 * eer) / 4, 2)
    carb_max_g = round((0.65 * eer) / 4, 2)

    return protein_min_g, protein_max_g, fat_min_g, fat_max_g, carb_min_g, carb_max_g


# -----------------------
# Vitamin & Mineral RDAs & AIs (Simplified Set)
# More can be added later
# -----------------------
def get_micronutrient_rdas(age, sex):
    # Basic version (can expand)
    vitamins = {
        "Vitamin A (mcg RAE)": 900 if sex == "male" else 700,
        "Vitamin C (mg)": 90 if sex == "male" else 75,
        "Vitamin D (mcg)": 20,
        "Vitamin E (mg)": 15,
        "Vitamin K (mcg)": 120 if sex == "male" else 90,
        "Vitamin B12 (mcg)": 2.4,
        "Folate (mcg)": 400,
    }

    minerals = {
        "Calcium (mg)": 1200 if age >= 70 else 1000,
        "Iron (mg)": 8 if sex == "male" else 18,
        "Magnesium (mg)": 420 if sex == "male" else 320,
        "Potassium (mg)": 3400 if sex == "male" else 2600,
        "Zinc (mg)": 11 if sex == "male" else 8,
        "Sodium (mg)": 1500
    }

    return vitamins, minerals
