from django.views.generic import ListView
from django.shortcuts import render

from .api import Fitbit


class ExercisesListView(ListView):
    fitbit_instance = Fitbit();
    initial = {'key': 'value'}
    template_name = 'exercises.html'

    def get(self, request, *args, **kwargs):

        auth_url = self.fitbit_instance.get_authorization_uri()

        return render(request, self.template_name, {'exercises': auth_url})

