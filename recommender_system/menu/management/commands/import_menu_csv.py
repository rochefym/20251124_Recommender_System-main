# menu/management/commands/import_menu_csv.py
import csv
import json
from django.core.management.base import BaseCommand
from menu.models import NutrientProfile, MenuItem, MenuDay

class Command(BaseCommand):
    help = "Import menu items from CSV and optionally create MenuDay mapping"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=str, help="Path to CSV file")
        parser.add_argument("--map-days", action="store_true", help="Optional: map days if day_index & meal_type present")

    def handle(self, *args, **options):
        path = options["csvfile"]
        map_days = options["map_days"]
        created = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # create or update NutrientProfile
                np_name = row.get("nutrient_profile_name") or row["name"]
                micron = {}
                mic_json = row.get("micronutrients_json") or "{}"
                try:
                    micron = json.loads(mic_json)
                except Exception:
                    self.stdout.write(self.style.WARNING(f"Invalid micronutrients JSON for {row['code']}, skipping micronutrients"))
                    micron = {}

                np, _ = NutrientProfile.objects.update_or_create(
                    name=np_name,
                    defaults={
                        "kcal_per_100g": float(row.get("kcal_per_100g") or 0),
                        "protein_g_per_100g": float(row.get("protein_g_per_100g") or 0),
                        "fat_g_per_100g": float(row.get("fat_g_per_100g") or 0),
                        "carbs_g_per_100g": float(row.get("carbs_g_per_100g") or 0),
                        "micronutrients": micron
                    }
                )

                mi, created_flag = MenuItem.objects.update_or_create(
                    code=row["code"],
                    defaults={
                        "name": row["name"],
                        "nutrient_profile": np,
                        "default_serving_g": float(row.get("default_serving_g") or 0)
                    }
                )
                created += 1

                # optionally create MenuDay mapping if columns day_index & meal_type exist
                if map_days and row.get("day_index") and row.get("meal_type"):
                    try:
                        day_index = int(row.get("day_index"))
                        meal_type = row.get("meal_type")
                        serving_g = row.get("serving_g")
                        MenuDay.objects.update_or_create(
                            day_index=day_index,
                            meal_type=meal_type,
                            menu_item=mi,
                            defaults={"serving_g": float(serving_g) if serving_g else None}
                        )
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Skipping day mapping for {mi.code}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Imported/updated {created} menu items."))
