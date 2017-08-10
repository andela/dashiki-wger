from django.conf.urls import url
from wger.fitbit.views import (
    ExercisesListView
)

urlpatterns = [
    url(r'^exercises/$', ExercisesListView.as_view(), name='exercises')
]
