import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import models after Django setup
from myapp.models import Food

# List of foods with nutritional information
# Format: name, carbs(g), protein(g), fats(g), calories
foods_to_add = [
    # Fruits
    ("Apple", 14, 0.3, 0.2, 52),
    ("Banana", 23, 1.1, 0.3, 89),
    ("Orange", 12, 0.9, 0.2, 47),
    ("Strawberries", 7.7, 0.7, 0.3, 32),
    ("Blueberries", 14, 0.7, 0.3, 57),
    ("Avocado", 9, 2, 15, 160),
    ("Mango", 15, 0.8, 0.4, 60),
    
    # Vegetables
    ("Broccoli", 6, 2.8, 0.4, 34),
    ("Spinach", 3.6, 2.9, 0.4, 23),
    ("Kale", 4.4, 2.9, 0.5, 33),
    ("Carrot", 10, 0.9, 0.2, 41),
    ("Sweet Potato", 20, 1.6, 0.1, 86),
    ("Bell Pepper", 6, 1, 0.3, 30),
    ("Cauliflower", 5, 2, 0.3, 25),
    
    # Proteins
    ("Chicken Breast", 0, 31, 3.6, 165),
    ("Salmon", 0, 20, 13, 206),
    ("Tuna", 0, 30, 1, 130),
    ("Eggs", 0.6, 6, 5, 78),
    ("Tofu", 2, 8, 4, 76),
    ("Greek Yogurt", 3.6, 10, 0.4, 59),
    ("Cottage Cheese", 3.4, 11, 4.3, 98),
    
    # Grains
    ("Brown Rice", 23, 2.6, 0.9, 112),
    ("Quinoa", 21, 4.4, 1.9, 120),
    ("Oatmeal", 27, 5, 3, 158),
    ("Whole Wheat Bread", 12, 3.6, 1, 69),
    ("Pasta", 25, 5, 1, 131),
    
    # Legumes
    ("Black Beans", 20, 8, 0.5, 114),
    ("Chickpeas", 27, 9, 3, 164),
    ("Lentils", 20, 9, 0.4, 116),
    
    # Nuts and Seeds
    ("Almonds", 6, 6, 14, 164),
    ("Walnuts", 4, 4, 18, 185),
    ("Chia Seeds", 12, 4, 9, 137),
    ("Flax Seeds", 8, 5, 10, 134),
    
    # Dairy
    ("Milk", 5, 3.4, 3.6, 65),
    ("Cheddar Cheese", 1.3, 7, 9, 113),
    
    # Snacks
    ("Dark Chocolate", 13, 2, 9, 136),
    ("Popcorn", 6, 1, 1, 31),
    ("Granola Bar", 18, 2, 6, 120),
    
    # Beverages
    ("Orange Juice", 10, 0.7, 0.2, 45),
    ("Green Tea", 0, 0, 0, 2),
    ("Coffee", 0, 0.1, 0, 2),
    
    # Fast Food
    ("Hamburger", 30, 15, 17, 354),
    ("Pizza (1 slice)", 35, 12, 10, 285),
    ("French Fries", 35, 3, 15, 312),
    ("Ice Cream", 24, 3.5, 11, 207),
    ("Chocolate Chip Cookie", 25, 2, 12, 200)
]

def add_foods():
    # Count of new foods added
    new_count = 0
    
    # Iterate through the foods list
    for food_data in foods_to_add:
        name, carbs, protein, fats, calories = food_data
        
        # Check if food already exists
        if not Food.objects.filter(name=name).exists():
            # Create new food
            Food.objects.create(
                name=name,
                carbs=carbs,
                protein=protein,
                fats=fats,
                calories=calories
            )
            new_count += 1
            print(f"Added: {name}")
        else:
            print(f"Skipped (already exists): {name}")
    
    print(f"\nAdded {new_count} new food items to the database.")

if __name__ == "__main__":
    print("Starting to add foods to the database...")
    add_foods()
    print("Finished adding foods to the database.")
