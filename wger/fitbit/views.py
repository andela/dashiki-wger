from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

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


@api_view(['GET'])
def get_fitbit_weight_data(request):
    '''
    Process the data to pass it to the JS libraries to generate an SVG image
    '''

    fitbit = Fitbit()
    current_user = request.user
    current_user_token = current_user.tokenmanager
    if not current_user_token or not current_user_token.has_fitbit_integration:
        auth_url = fitbit.get_authorization_uri()

        return redirect(auth_url)

    data = fitbit.api_call(
        current_user_token,
        '/1/user/-/body/weight/date/today/3m.json')
    print(data['body-weight'])
    return Response(data['body-weight'])
