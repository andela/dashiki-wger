from django.apps import AppConfig

class NutritionPlanConfig(AppConfig):
    name = 'wger.nutrition'
    verbose_name = 'nutrition'

    def ready(self):
        import wger.nutrition.signals
        