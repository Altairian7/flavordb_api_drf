# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'user-meals', views.UserMealViewSet)
router.register(r'taste-profiles', views.TasteProfileViewSet)
router.register(r'beverage-pairings', views.BeveragePairingViewSet)
router.register(r'healthy-swaps', views.HealthySwapViewSet)
router.register(r'compounds', views.CompoundViewSet)

urlpatterns = [
    path('', include(router.urls)),
]