from django.conf.urls import url
from wger.fitbit.views import (
    ExercisesListView,
    FitbitAuthentication
)

urlpatterns = [
    url(r'^exercises/$', ExercisesListView.as_view(), name='exercises'),
    url(r'^login/$', FitbitAuthentication.as_view(), name='login')
]
