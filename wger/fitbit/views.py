from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .api import Fitbit
from wger.fitbit.models import TokenManager


class ExercisesListView(ListView):
    initial = {'key': 'value'}
    template_name = 'exercises.html'
    fitbit = Fitbit()

    def get(self, request, *args, **kwargs):
        current_user = request.user
        current_user_token =\
            TokenManager.objects.filter(user=current_user).first()

        if not current_user_token or current_user_token.has_fitbit_integration:
            auth_url = self.fitbit.get_authorization_uri()

            return redirect(auth_url)

        return render(
            request, self.template_name,
            {'exercises': 'Do api integration'}
        )


class FitbitAuthentication(ListView):
    fitbit = Fitbit()
    initial = {'key': 'value'}
    template_name = 'exercises.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        access_code = request.GET['code']
        self.fitbit.get_access_token(access_code, current_user)

        return render(request, self.template_name, {'exercises': 'Successful'})


# def get(self, request, *args, **kwargs):
#
#     auth_url = self.fitbit.get_authorization_uri()
#
#     # return render(request, self.template_name, {'exercises': auth_url})
#     return redirect(auth_url)
