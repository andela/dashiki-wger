import datetime
from django.core.cache import cache
from wger.utils.cache import cache_mapper
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.nutrition.models import NutritionPlan


class NutritionInfoCacheTestCase(WorkoutManagerTestCase):
    '''
    Test case for the nutrition info caching
    '''

    def test_meal_nutritional_info_cache(self):
        '''
        Tests that the nutrition cache of the canonical form is
        correctly generated
        '''
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values(1)))

        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values(1)))

    def test_nutrition_info_cache_save(self):
        '''
        Tests nutritional info cache when saving
        '''
        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values(1)))

        plan.save()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values(1)))

    def test_nutrition_info_cache_delete(self):
        '''
        Tests the nutritional info cache when deleting
        '''
        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values(1)))

        plan.delete()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values(1)))
