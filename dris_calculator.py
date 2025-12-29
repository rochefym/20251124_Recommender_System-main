


#Calculates BMI
def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    bmi = weight_kg / (height_m ** 2)
    return bmi

#Calculates EER
def calculate_eer(age, gender, weight_kg, height_cm, physical_activity_level):
    if gender.lower() == 'male':                    
        eer = 662 - (9.53 * age) + physical_activity_level * (15.91 * weight_kg + 539.6 * height_cm / 100)
    elif gender.lower() == 'female':
        eer = 354 - (6.91 * age) + physical_activity_level * (9.36 * weight_kg + 726 * height_cm / 100)         
    else:
        raise ValueError("Gender must be 'male' or 'female'.")
    return eer
    

#Calculates AMDR
def calculate_amdr(eer):
    protein_min = 0.10 * eer / 4
    protein_max = 0.35 * eer / 4
    fat_min = 0.20 * eer / 9
    fat_max = 0.35 * eer / 9
    carb_min = 0.45 * eer / 4
    carb_max = 0.65 * eer / 4
    return {
        'protein': (protein_min, protein_max),
        'fat': (fat_min, fat_max),
        'carbohydrate': (carb_min, carb_max)
    }
    
