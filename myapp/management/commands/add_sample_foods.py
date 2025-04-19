from django.core.management.base import BaseCommand
from myapp.models import Food

class Command(BaseCommand):
    help = 'Adds sample food items to the database'

    def handle(self, *args, **options):
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

        # Check if foods already exist
        if Food.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Food items already exist in the database.'))
            return
        
        # Add sample foods
        for food_data in sample_foods:
            food = Food(**food_data)
            food.save()
            self.stdout.write(self.style.SUCCESS(f'Added {food.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(sample_foods)} food items to the database.'))
