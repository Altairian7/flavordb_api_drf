# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_records = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

class Meal(models.Model):
    name = models.CharField(max_length=200)
    recipe = models.TextField()
    nutritional_info = models.JSONField()
    ingredients = models.JSONField()
    weather_suitable = models.CharField(max_length=100, blank=True)
    season_suitable = models.CharField(max_length=100, blank=True)

class UserMeal(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

class TasteProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    compound_preferences = models.JSONField()
    taste_vector = models.JSONField()

class BeveragePairing(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    beverage = models.CharField(max_length=200)
    pairing_notes = models.TextField()

class HealthySwap(models.Model):
    original_ingredient = models.CharField(max_length=200)
    healthy_alternative = models.CharField(max_length=200)
    nutritional_difference = models.JSONField()

class Compound(models.Model):
    compound_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    taste_profile = models.JSONField()