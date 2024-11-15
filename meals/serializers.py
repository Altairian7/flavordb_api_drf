# serializers.py
from rest_framework import serializers
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class UserMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMeal
        fields = '__all__'

class TasteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteProfile
        fields = '__all__'

class BeveragePairingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeveragePairing
        fields = '__all__'

class HealthySwapSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthySwap
        fields = '__all__'

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = '__all__'