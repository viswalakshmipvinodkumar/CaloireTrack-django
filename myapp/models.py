from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Food(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()


class Consume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1.0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} consumed {self.quantity} {self.food_consumed.name}"
    
    # Calculate adjusted nutritional values based on quantity
    @property
    def adjusted_calories(self):
        return int(self.food_consumed.calories * self.quantity)
    
    @property
    def adjusted_carbs(self):
        return round(self.food_consumed.carbs * self.quantity, 1)
    
    @property
    def adjusted_protein(self):
        return round(self.food_consumed.protein * self.quantity, 1)
    
    @property
    def adjusted_fats(self):
        return round(self.food_consumed.fats * self.quantity, 1)


class NutritionGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_calories = models.IntegerField(default=2000)
    carbs_percent = models.IntegerField(default=50)
    protein_percent = models.IntegerField(default=30)
    fat_percent = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Nutrition Goals"
    
    @property
    def daily_carbs_grams(self):
        """Calculate daily carbs in grams based on percentage and calorie goal"""
        return round((self.daily_calories * (self.carbs_percent / 100)) / 4)
    
    @property
    def daily_protein_grams(self):
        """Calculate daily protein in grams based on percentage and calorie goal"""
        return round((self.daily_calories * (self.protein_percent / 100)) / 4)
    
    @property
    def daily_fat_grams(self):
        """Calculate daily fat in grams based on percentage and calorie goal"""
        return round((self.daily_calories * (self.fat_percent / 100)) / 9)


# Meal Planning Models
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date', 'name']

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    @property
    def total_calories(self):
        return sum(item.adjusted_calories for item in self.mealitem_set.all())
    
    @property
    def total_carbs(self):
        return sum(item.adjusted_carbs for item in self.mealitem_set.all())
    
    @property
    def total_protein(self):
        return sum(item.adjusted_protein for item in self.mealitem_set.all())
    
    @property
    def total_fats(self):
        return sum(item.adjusted_fats for item in self.mealitem_set.all())


class MealItem(models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    )
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    quantity = models.FloatField(default=1.0)
    notes = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.food.name} - {self.get_meal_type_display()}"
    
    @property
    def adjusted_calories(self):
        return round(self.food.calories * self.quantity)
    
    @property
    def adjusted_carbs(self):
        return round(self.food.carbs * self.quantity, 1)
    
    @property
    def adjusted_protein(self):
        return round(self.food.protein * self.quantity, 1)
    
    @property
    def adjusted_fats(self):
        return round(self.food.fats * self.quantity, 1)
