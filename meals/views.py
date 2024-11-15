# meals/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .services.taste_profile_service import TasteProfileService, Beverage

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['post'])
    def add_favorite_meal(self, request, pk=None):
        profile = self.get_object()
        meal_id = request.data.get('meal_id')
        UserMeal.objects.create(user=profile, meal_id=meal_id, is_favorite=True)
        return Response({'status': 'meal added to favorites'})

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=['get'])
    def get_beverage_pairings(self, request, pk=None):
        meal = self.get_object()
        pairings = BeveragePairing.objects.filter(meal=meal)
        return Response({'pairings': [{'beverage': p.beverage, 'notes': p.pairing_notes} for p in pairings]})

    @action(detail=True, methods=['get'])
    def get_healthy_swaps(self, request, pk=None):
        meal = self.get_object()
        # Logic to find healthy swaps for meal ingredients
        return Response({'healthy_swaps': []})

class UserMealViewSet(viewsets.ModelViewSet):
    queryset = UserMeal.objects.all()
    serializer_class = UserMealSerializer

class TasteProfileViewSet(viewsets.ModelViewSet):
    queryset = TasteProfile.objects.all()
    serializer_class = TasteProfileSerializer

    @action(detail=True, methods=['post'])
    def create_from_favorites(self, request, pk=None):
        profile = self.get_object()
        favorite_dish_ids = request.data.get('favorite_dish_ids', [])
        favorite_dishes = Meal.objects.filter(id__in=favorite_dish_ids)
        
        service = TasteProfileService()
        taste_profile = service.create_user_taste_profile(favorite_dishes)
        
        profile.compound_preferences = taste_profile['compound_preferences']
        profile.taste_vector = taste_profile['taste_vector']
        profile.save()
        
        return Response(self.get_serializer(profile).data)

class BeveragePairingViewSet(viewsets.ModelViewSet):
    queryset = BeveragePairing.objects.all()
    serializer_class = BeveragePairingSerializer

    @action(detail=False, methods=['post'])
    def get_recommendations(self, request):
        user_profile = request.user.taste_profile
        current_dish = Meal.objects.get(id=request.data.get('dish_id'))
        beverages = Beverage.objects.all()
        
        service = TasteProfileService()
        recommendations = service.calculate_beverage_compatibility(
            user_profile,
            current_dish,
            beverages
        )
        
        return Response({
            'recommendations': [
                {
                    'beverage_id': rec['beverage'].id,
                    'name': rec['beverage'].name,
                    'score': rec['score'],
                    'taste_similarity': rec['taste_similarity'],
                    'compound_overlap': rec['compound_overlap']
                }
                for rec in recommendations[:5]
            ]
        })

class HealthySwapViewSet(viewsets.ModelViewSet):
    queryset = HealthySwap.objects.all()
    serializer_class = HealthySwapSerializer

class CompoundViewSet(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer