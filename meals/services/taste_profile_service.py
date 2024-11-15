# taste_profile_service.py
from typing import List, Dict
import numpy as np
from scipy.spatial.distance import cosine
import requests

class Meal:
    def __init__(self, compounds, taste_vector):
        self.compounds = compounds  # List of Compound objects
        self.taste_vector = taste_vector  # Taste vector as a list of floats


class TasteProfile:
    def __init__(self, taste_vector, compound_preferences):
        self.taste_vector = taste_vector  # User's taste vector
        self.compound_preferences = compound_preferences  # Dict of compound preferences

class Beverage:
    def __init__(self, compounds, taste_vector):
        self.compounds = compounds  # List of Compound objects
        self.taste_vector = taste_vector  # Taste vector as a list of floats

class TasteProfileService:
    def __init__(self):
        self.taste_dimensions = [
            'sweet', 'bitter', 'sour', 'salty', 'umami',
            'spicy', 'fatty', 'woody', 'floral', 'fruity'
        ]

    def fetch_flavor_compounds(self, ingredient: str) -> List[Dict]:
        """Fetch compound data from FlavorDB API"""
        api_url = "https://flavordb.org/api/ingredients/search"
        response = requests.get(f"{api_url}?query={ingredient}")
        return response.json()

    def create_user_taste_profile(self, favorite_dishes: List[Meal]) -> Dict:
        """Create a user taste profile from favorite dishes"""
        compound_frequencies = {}
        taste_vector = np.zeros(len(self.taste_dimensions))

        for dish in favorite_dishes:
            for compound in dish.compounds.all():
                compound_id = compound.compound_id
                compound_frequencies[compound_id] = compound_frequencies.get(compound_id, 0) + 1

            dish_vector = np.array(dish.taste_vector)
            taste_vector += dish_vector

        taste_vector = taste_vector / len(favorite_dishes)

        return {
            'compound_preferences': compound_frequencies,
            'taste_vector': taste_vector.tolist()
        }

    def calculate_beverage_compatibility(
        self,
        user_profile: TasteProfile,
        current_dish: Meal,
        beverages: List[Beverage]
    ) -> List[Dict]:
        """Calculate compatibility scores for beverages"""
        combined_vector = np.mean([
            user_profile.taste_vector,
            current_dish.taste_vector
        ], axis=0)

        compatibility_scores = []

        for beverage in beverages:
            taste_similarity = 1 - cosine(combined_vector, beverage.taste_vector)

            user_compounds = set(user_profile.compound_preferences.keys())
            dish_compounds = {c.compound_id for c in current_dish.compounds.all()}
            beverage_compounds = {c.compound_id for c in beverage.compounds.all()}

            compound_overlap = len(
                (user_compounds | dish_compounds) & beverage_compounds
            ) / len(beverage_compounds)

            final_score = 0.7 * taste_similarity + 0.3 * compound_overlap

            compatibility_scores.append({
                'beverage': beverage,
                'score': final_score,
                'taste_similarity': taste_similarity,
                'compound_overlap': compound_overlap
            })

        return sorted(compatibility_scores, key=lambda x: x['score'], reverse=True)