from django.conf.urls import url
from wger.fitbit.views import (
    WeightsListView,
    FitbitAuthentication
)

urlpatterns = [
    url(r'^fitbit_weights/$', WeightsListView.as_view(), name='weights'),
    url(r'^login/$', FitbitAuthentication.as_view(), name='login')
]
