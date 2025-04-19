import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import models after Django setup
from myapp.models import Food

# Sample food data
sample_foods = [
    {'name': 'Apple', 'carbs': 14, 'protein': 0.3, 'fats': 0.2, 'calories': 52},
    {'name': 'Banana', 'carbs': 23, 'protein': 1.1, 'fats': 0.3, 'calories': 89},
    {'name': 'Chicken Breast', 'carbs': 0, 'protein': 31, 'fats': 3.6, 'calories': 165},
    {'name': 'Egg', 'carbs': 0.6, 'protein': 6.3, 'fats': 5.3, 'calories': 78},
    {'name': 'Rice (cooked)', 'carbs': 28, 'protein': 2.7, 'fats': 0.3, 'calories': 130},
    {'name': 'Bread (1 slice)', 'carbs': 13, 'protein': 4, 'fats': 1, 'calories': 79},
    {'name': 'Milk (1 cup)', 'carbs': 12, 'protein': 8, 'fats': 8, 'calories': 149},
    {'name': 'Oatmeal', 'carbs': 27, 'protein': 5, 'fats': 3, 'calories': 158},
    {'name': 'Salmon (100g)', 'carbs': 0, 'protein': 25, 'fats': 13, 'calories': 208},
    {'name': 'Avocado (half)', 'carbs': 6, 'protein': 2, 'fats': 15, 'calories': 161}
]

def add_sample_foods():
    # Check if foods already exist
    if Food.objects.count() > 0:
        print("Food items already exist in the database.")
        return
    
    # Add sample foods
    for food_data in sample_foods:
        food = Food(**food_data)
        food.save()
        print(f"Added {food.name}")
    
    print(f"Successfully added {len(sample_foods)} food items to the database.")

if __name__ == "__main__":
    add_sample_foods()
