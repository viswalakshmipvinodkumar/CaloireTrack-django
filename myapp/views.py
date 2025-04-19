from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Consume, NutritionGoal, MealPlan, MealItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime
import pytz
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def home(request):
    """Home page view with site introduction"""
    return render(request, 'myapp/home.html')


def user_login(request):
    """Handle user login using Django's built-in AuthenticationForm"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'myapp/login.html', {'form': form})


def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Create default nutrition goals for new user
        NutritionGoal.objects.create(user=user)
        
        messages.success(request, f'Account created for {username}! You can now log in.')
        return redirect('login')
    
    return render(request, 'myapp/register.html')


@login_required
def profile(request):
    """User profile view"""
    # Get or create nutrition goals for the user
    goals, created = NutritionGoal.objects.get_or_create(user=request.user)
    
    # Handle form submission for updating goals
    if request.method == 'POST':
        # Get form data
        daily_calories = request.POST.get('daily_calories')
        carbs_percent = request.POST.get('carbs_percent')
        protein_percent = request.POST.get('protein_percent')
        fat_percent = request.POST.get('fat_percent')
        
        # Validate data
        try:
            daily_calories = int(daily_calories)
            carbs_percent = int(carbs_percent)
            protein_percent = int(protein_percent)
            fat_percent = int(fat_percent)
            
            # Check if percentages add up to 100
            if carbs_percent + protein_percent + fat_percent != 100:
                messages.error(request, 'Macronutrient percentages must add up to 100%.')
            else:
                # Update goals
                goals.daily_calories = daily_calories
                goals.carbs_percent = carbs_percent
                goals.protein_percent = protein_percent
                goals.fat_percent = fat_percent
                goals.save()
                
                messages.success(request, 'Nutrition goals updated successfully!')
        except ValueError:
            messages.error(request, 'Please enter valid numbers for all fields.')
    
    # Get recent consumed items
    recent_items = Consume.objects.filter(user=request.user).order_by('-id')[:5]
    
    context = {
        'goals': goals,
        'recent_items': recent_items
    }
    
    return render(request, 'myapp/profile.html', context)


def index(request):
    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        quantity = float(request.POST.get('quantity', 1))
        consume = Food.objects.get(name=food_consumed)
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
            
        consume_obj = Consume(
            user=user,
            food_consumed=consume,
            quantity=quantity
        )
        consume_obj.save()
        messages.success(request, f'Added {quantity} serving(s) of {food_consumed} to your log')
        return redirect('index')
    
    # Get all foods and consumed foods
    foods = Food.objects.all()
    
    # Set default calorie goal
    calorie_goal = 2000
    
    # If user is authenticated, get their consumed foods and calorie goal
    if request.user.is_authenticated:
        consumed_food = Consume.objects.filter(user=request.user)
        
        # Get user's calorie goal from NutritionGoal if it exists
        try:
            nutrition_goal = NutritionGoal.objects.get(user=request.user)
            calorie_goal = nutrition_goal.daily_calories
        except NutritionGoal.DoesNotExist:
            # Create default nutrition goal for user
            nutrition_goal = NutritionGoal.objects.create(user=request.user)
            calorie_goal = nutrition_goal.daily_calories
    else:
        consumed_food = Consume.objects.filter(user=None)
    
    context = {
        'foods': foods,
        'consumed_food': consumed_food,
        'calorie_goal': calorie_goal
    }
    return render(request, 'myapp/index.html', context)


def delete(request, id):
    try:
        consume = Consume.objects.get(id=id)
        if request.method == 'POST':
            consume.delete()
            messages.success(request, 'Food item deleted successfully')
            return redirect('index')
        return render(request, 'myapp/delete.html', {'consume': consume})
    except Consume.DoesNotExist:
        return redirect('/')


# Meal Planning Views
@login_required
def meal_plans(request):
    """View all meal plans for the current user"""
    meal_plans = MealPlan.objects.filter(user=request.user)
    
    context = {
        'meal_plans': meal_plans,
    }
    return render(request, 'myapp/meal_plans.html', context)


@login_required
def meal_plan_detail(request, plan_id):
    """View details of a specific meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    
    # Group meal items by meal type
    breakfast_items = meal_plan.mealitem_set.filter(meal_type='breakfast')
    lunch_items = meal_plan.mealitem_set.filter(meal_type='lunch')
    dinner_items = meal_plan.mealitem_set.filter(meal_type='dinner')
    snack_items = meal_plan.mealitem_set.filter(meal_type='snack')
    
    context = {
        'meal_plan': meal_plan,
        'breakfast_items': breakfast_items,
        'lunch_items': lunch_items,
        'dinner_items': dinner_items,
        'snack_items': snack_items,
    }
    return render(request, 'myapp/meal_plan_detail.html', context)


@login_required
def create_meal_plan(request):
    """Create a new meal plan"""
    if request.method == 'POST':
        name = request.POST.get('name')
        date_str = request.POST.get('date')
        notes = request.POST.get('notes', '')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Create the meal plan
            meal_plan = MealPlan.objects.create(
                user=request.user,
                name=name,
                date=date_obj,
                notes=notes
            )
            
            messages.success(request, f'Meal plan "{name}" created successfully')
            return redirect('meal_plan_detail', plan_id=meal_plan.id)
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD')
    
    # For GET request, just render the form
    context = {
        'today': datetime.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'myapp/create_meal_plan.html', context)


@login_required
def add_meal_item(request, plan_id):
    """Add a food item to a meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    foods = Food.objects.all()
    
    if request.method == 'POST':
        food_id = request.POST.get('food')
        meal_type = request.POST.get('meal_type')
        quantity = float(request.POST.get('quantity', 1))
        notes = request.POST.get('notes', '')
        
        food = get_object_or_404(Food, id=food_id)
        
        # Create the meal item
        MealItem.objects.create(
            meal_plan=meal_plan,
            food=food,
            meal_type=meal_type,
            quantity=quantity,
            notes=notes
        )
        
        messages.success(request, f'Added {food.name} to {meal_plan.name}')
        return redirect('meal_plan_detail', plan_id=meal_plan.id)
    
    context = {
        'meal_plan': meal_plan,
        'foods': foods,
        'meal_types': MealItem.MEAL_TYPES,
    }
    return render(request, 'myapp/add_meal_item.html', context)


@login_required
def delete_meal_item(request, item_id):
    """Delete a meal item from a meal plan"""
    meal_item = get_object_or_404(MealItem, id=item_id)
    meal_plan = meal_item.meal_plan
    
    # Ensure the meal plan belongs to the current user
    if meal_plan.user != request.user:
        messages.error(request, 'You do not have permission to delete this item')
        return redirect('meal_plans')
    
    if request.method == 'POST':
        meal_item.delete()
        messages.success(request, f'Removed {meal_item.food.name} from {meal_plan.name}')
        return redirect('meal_plan_detail', plan_id=meal_plan.id)
    
    context = {
        'meal_item': meal_item,
        'meal_plan': meal_plan,
    }
    return render(request, 'myapp/delete_meal_item.html', context)


@login_required
def delete_meal_plan(request, plan_id):
    """Delete an entire meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        meal_plan.delete()
        messages.success(request, f'Meal plan "{meal_plan.name}" deleted successfully')
        return redirect('meal_plans')
    
    context = {
        'meal_plan': meal_plan,
    }
    return render(request, 'myapp/delete_meal_plan.html', context)


# Data Visualization Dashboard
@login_required
def dashboard(request):
    """Dashboard with data visualizations of nutrition and consumption patterns"""
    # Get user's consumed foods for the last 30 days
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    consumed_items = Consume.objects.filter(
        user=request.user
    )
    
    # Get user's nutrition goals
    nutrition_goal, created = NutritionGoal.objects.get_or_create(user=request.user)
    
    # Prepare data for charts
    # 1. Daily calorie intake over time
    dates = []
    daily_calories = []
    daily_carbs = []
    daily_proteins = []
    daily_fats = []
    
    # Group by date and calculate totals
    from django.db.models import Sum
    
    # 2. Most consumed foods
    from django.db.models import Count
    
    most_consumed = consumed_items.values(
        'food_consumed__name'
    ).annotate(
        count=Count('food_consumed')
    ).order_by('-count')[:10]
    
    food_names = [item['food_consumed__name'] for item in most_consumed]
    food_counts = [item['count'] for item in most_consumed]
    
    # 3. Average macronutrient distribution
    if consumed_items:
        total_carbs = 0
        total_proteins = 0
        total_fats = 0
        
        total_macros = total_carbs + total_proteins + total_fats
        
        if total_macros > 0:
            avg_carbs_pct = round((total_carbs / total_macros) * 100)
            avg_proteins_pct = round((total_proteins / total_macros) * 100)
            avg_fats_pct = round((total_fats / total_macros) * 100)
        else:
            avg_carbs_pct = 0
            avg_proteins_pct = 0
            avg_fats_pct = 0
    else:
        avg_carbs_pct = 0
        avg_proteins_pct = 0
        avg_fats_pct = 0
    
    # 4. Goal achievement statistics
    days_over_goal = 0
    days_under_goal = 0
    days_at_goal = 0
    
    context = {
        # Chart data
        'dates': dates,
        'daily_calories': daily_calories,
        'daily_carbs': daily_carbs,
        'daily_proteins': daily_proteins,
        'daily_fats': daily_fats,
        'food_names': food_names,
        'food_counts': food_counts,
        'avg_carbs_pct': avg_carbs_pct,
        'avg_proteins_pct': avg_proteins_pct,
        'avg_fats_pct': avg_fats_pct,
        
        # Goal statistics
        'days_over_goal': days_over_goal,
        'days_under_goal': days_under_goal,
        'days_at_goal': days_at_goal,
        'total_days': len(daily_calories),
        
        # User's goals
        'nutrition_goal': nutrition_goal,
    }
    
    return render(request, 'myapp/dashboard.html', context)
