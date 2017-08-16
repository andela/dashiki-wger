from django.conf.urls import url
from wger.fitbit.views import (
    WeightsListView,
    FitbitAuthentication,
    get_fitbit_weight_data
)

urlpatterns = [
    url(r'^fitbit_weights/$', WeightsListView.as_view(), name='weights'),
    url(r'^login/$', FitbitAuthentication.as_view(), name='login'),
    url(r'^get_fitbit_weight_data/$',  # JS
        get_fitbit_weight_data,
        name='fitbit-weight-data'),
]
