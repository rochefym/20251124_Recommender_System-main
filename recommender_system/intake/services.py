def calculate_intake(meal, consumed_weight_g=None, consumed_volume_ml=None):
    # Determine scaling factor
    if consumed_weight_g:
        factor = consumed_weight_g / meal.weight_g
    elif consumed_volume_ml:
        factor = consumed_volume_ml / meal.volume_ml
    else:
        factor = 1.0

    nutrients = {
        "calories": round(meal.calories * factor, 2),
        "protein": round(meal.protein * factor, 2),
        "fat": round(meal.fat * factor, 2),
        "carbs": round(meal.carbs * factor, 2),
        "vitamins": {k: round(v * factor, 2) for k, v in meal.vitamins.items()},
        "minerals": {k: round(v * factor, 2) for k, v in meal.minerals.items()},
    }

    return nutrients
