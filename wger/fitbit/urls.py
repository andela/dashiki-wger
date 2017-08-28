from django.conf.urls import url
from wger.fitbit.views import (
    WeightsListView,
    FitbitAuthentication,
    ActivitiesListView,
    get_fitbit_weight_data
)

urlpatterns = [
    url(r'^fitbit_weights/$', WeightsListView.as_view(), name='weights'),
    url(r'^fitbit_activities/$', ActivitiesListView.as_view(), name='activities'),
    url(r'^login/$', FitbitAuthentication.as_view(), name='login'),
    url(r'^get_fitbit_weight_data/$',
        get_fitbit_weight_data,
        name='fitbit-weight-data'),
]
