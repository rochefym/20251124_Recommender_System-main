# recommendations/services.py
from datetime import date, timedelta
from menu.models import MenuItem, MenuDay
from intake.models import IntakeRecord
from dri.services import calculate_eer  # your existing function to produce calorie/macros/micros targets
from .models import Recommendation
import requests
import os
from dri.services import (
    calculate_bmi, calculate_eer,
    calculate_macros, get_micronutrient_rdas
)


def calculate_dri(sex, age, height_cm, weight_kg, activity_level):
    # ---- Calculations ----
    bmi = calculate_bmi(weight_kg, height_cm)
    eer = calculate_eer(age, sex, weight_kg, height_cm, activity_level)
    protein_min_g, protein_max_g, fat_min_g, fat_max_g, carb_min_g, carb_max_g = calculate_macros(eer)
    vitamins, minerals = get_micronutrient_rdas(age, sex)

    result = {
        "bmi": bmi,
        "eer": eer,
        "protein_g": {
            "protein_min_10": protein_min_g, 
            "protein_max_35": protein_max_g
            },
        "fat_g": {
            "fat_min_20": fat_min_g, 
            "fat_max_35": fat_max_g
            },
        "carbs_g": {
            "carb_min_45": carb_min_g,
            "carb_max_65":  carb_max_g
            },
        "vitamins": vitamins,
        "minerals": minerals,
    }

    return result


# Configuration: your GPU-hosted RAG/LLM endpoint
RAG_API_BASE = os.environ.get("RAG_API_BASE", "http://gpu-server.example.com:8000")  # change to your host
RAG_API_GENERATE = f"{RAG_API_BASE}/generate"  # example endpoint; adapt to your server's API

def aggregate_intake(user, start_date, end_date):
    """
    aggregate nutrients between start_date and end_date inclusive
    returns dict of nutrients sums per day averaged if needed
    """
    records = IntakeRecord.objects.filter(user=user, created_at__date__gte=start_date, created_at__date__lte=end_date)
    total = {}
    days = (end_date - start_date).days + 1
    for r in records:
        nutrients = r.calculated_nutrients or {}
        for k, v in nutrients.items():
            total[k] = total.get(k, 0) + (v or 0)
    # optionally return average per day
    return {"total": total, "days": days, "average_per_day": {k: round(v / days, 2) for k, v in total.items()}}


# Simple heuristic rules to create candidate suggestions before calling LLM
def simple_rule_recs(targets, intake_avg):
    alerts = []
    suggestions = []
    # calories
    tcal = targets["calories"]
    ical = intake_avg.get("calories", 0)
    pct = ical / tcal if tcal else 0
    if pct < 0.85:
        alerts.append(f"Average daily calories intake is low ({int(ical)} kcal vs target {int(tcal)} kcal).")
        suggestions.append("Offer high-calorie nutrient-dense snacks (e.g., milk, soy-sauce braised tofu, peanut paste).")
    if pct > 1.2:
        alerts.append("Average daily intake is high.")
        suggestions.append("Consider reducing high-fat snacks or portion sizes.")

    # protein
    tp = targets["macros"]["protein_g"]
    ip = intake_avg.get("protein_g", 0)
    ppct = ip / tp if tp else 0
    if ppct < 0.85:
        alerts.append(f"Average protein is low ({int(ip)}g vs target {int(tp)}g).")
        suggestions.append("Add extra protein at meals: 1 egg, 50g tofu, or 20g powdered milk per serving.")

    # micronutrient simple checks: compare keys intersection
    for micron, mval in (targets.get("micronutrients") or {}).get("vitamins", {}).items():
        intake_val = intake_avg.get(micron, 0)
        if mval and intake_val and (intake_val / mval) < 0.7:
            alerts.append(f"Low {micron} — {int(intake_val)} vs {mval}{targets.get('micronutrients').get('units', '')}")
            suggestions.append(f"Provide {recommend_food_for_nutrient(micron)}.")

    return {"alerts": alerts, "suggestions": suggestions}


def recommend_food_for_nutrient(nutrient_name):
    # quick mapping — expand with local foods for Taiwan
    map_food = {
        "Vitamin C (mg)": "fresh citrus, guava, or steamed broccoli",
        "Calcium (mg)": "tofu, small fish with bones, soy milk",
        "Vitamin D (IU)": "sunlight exposure and fortified milk or fish"
    }
    return map_food.get(nutrient_name, "berries, leafy greens, legumes")

# Calls external LLM/RAG to convert structured context+rules into a polished recommendation
def call_rag_for_recommendation(context: dict) -> dict:
    """
    context: {
      "user": {...},
      "targets": {...},
      "intake_avg": {...},
      "rule_candidates": {"alerts": [...], "suggestions": [...]}
    }
    """
    payload = {
        "prompt_type": "recommendation_generation",
        "context": context
    }
    try:
        resp = requests.post(RAG_API_GENERATE, json=payload, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # fallback: return a basic text
        return {
            "text": "Unable to reach RAG server; use rule-based suggestions.",
            "structured": context["rule_candidates"]
        }


def generate_recommendation(user, period="daily", ref_date=None):
    """
    period: 'daily' (1 day), 'weekly' (7 days), 'monthly' (30 days)
    """
    if not ref_date:
        ref_date = date.today()

    if period == "daily":
        start = ref_date
    elif period == "weekly":
        start = ref_date - timedelta(days=6)
    elif period == "monthly":
        start = ref_date - timedelta(days=29)
    else:
        start = ref_date

    # compute targets using calculate_eer (expects patient/user profile)
    targets = calculate_eer(user)  

    # aggregate intake
    agg = aggregate_intake(user, start, ref_date)
    intake_avg = agg["average_per_day"]

    # build simple rule suggestions
    rule_candidates = simple_rule_recs(targets, intake_avg)

    # build context for RAG
    context = {
        "user": {
            "name": getattr(user, "name", ""),
            "age": getattr(user, "age", None),
            "sex": getattr(user, "sex", "")
        },
        "period": period,
        "date_range": {"start": start.isoformat(), "end": ref_date.isoformat()},
        "targets": {
            "calories": round(targets["calories"], 2),
            "macros": targets["macros"],
            "micronutrients": targets.get("micronutrients", {})
        },
        "intake_avg": intake_avg,
        "rule_candidates": rule_candidates
    }

    # call LLM/RAG for polished advice + citations
    rag_res = call_rag_for_recommendation(context)

    # persist as Recommendation DB record
    rec = Recommendation.objects.create(
        user=user,
        period=period,
        suggestions=rag_res.get("text") or "\n".join(rule_candidates.get("suggestions", []))
    )
    return {"recommendation": rag_res, "saved_id": rec.id}
