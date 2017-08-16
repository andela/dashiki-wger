from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .api import Fitbit
from wger.fitbit.models import TokenManager


class WeightsListView(ListView):
    initial = {'key': 'value'}
    template_name = 'weights.html'
    fitbit = Fitbit()

    def get(self, request, *args, **kwargs):
        current_user = request.user
        current_user_token = current_user.tokenmanager
        if not current_user_token or not current_user_token.has_fitbit_integration:
            auth_url = self.fitbit.get_authorization_uri()

            return redirect(auth_url)

        return render(
            request, self.template_name,
            {'weights': self.fitbit.api_call(
                current_user_token,
                '/1/user/-/body/weight/date/today/1w.json')}
        )


class FitbitAuthentication(ListView):
    fitbit = Fitbit()
    initial = {'key': 'value'}
    template_name = 'weights.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        access_code = request.GET['code']
        self.fitbit.get_access_token(access_code, current_user)

        return render(request, self.template_name, {'weights': 'Successful'})

