from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver
from wger.nutrition.models import NutritionPlan, Meal, MealItem
from wger.utils.cache import reset_nutritional_values


@receiver(post_save, sender=NutritionPlan)
@receiver(post_save, sender=Meal)
@receiver(post_save, sender=MealItem)
@receiver(post_delete, sender=NutritionPlan)
@receiver(post_delete, sender=Meal)
@receiver(post_delete, sender=MealItem)
def delete_cache(sender, **kwargs):
    model_instance = kwargs['instance']
    if sender == NutritionPlan:
        pk = model_instance.pk
    elif sender == Meal:
        pk = model_instance.plan.pk
    elif sender == MealItem:
        pk = model_instance.meal.plan.pk

    reset_nutritional_values(pk)
