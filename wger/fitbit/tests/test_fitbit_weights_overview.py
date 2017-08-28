import mock
from django.core.urlresolvers import reverse
from mock import patch
from django.contrib import auth

from wger.fitbit.api import Fitbit
from wger.fitbit.models import TokenManager
from django.conf import settings
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class FitbitWeightsTestCase(WorkoutManagerTestCase):
    SITE_URL = settings.SITE_URL
    fitbit = Fitbit()

    @patch('wger.fitbit.api.requests.get')
    def test_fitbit_weights_overview(self, mock_api_call):
        # authorize_token_url calls oauth and returns a URL
        self.user_login()
        mock_response = mock.Mock()
        expected_dict = \
            {
                'body-weight':
                    [
                        {'dateTime': '2017-08-12', 'value': '83.0'},
                        {'dateTime': '2017-08-13', 'value': '85.5'},
                        {'dateTime': '2017-08-14', 'value': '88.0'},
                        {'dateTime': '2017-08-15', 'value': '90.5'},
                        {'dateTime': '2017-08-16', 'value': '93.0'},
                        {'dateTime': '2017-08-17', 'value': '95.5'},
                        {'dateTime': '2017-08-18', 'value': '98.0'}
                    ]
            }
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_api_call.return_value = mock_response

        user = auth.get_user(self.client)
        user_token = TokenManager(
            refresh_token='refresh_token',
            access_token='access_token',
            user=user,
            has_fitbit_integration=True
        )

        user_token.save()
        response = self.client.get(
            self.SITE_URL + reverse('fitbit:weights'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weights.html')
        self.assertContains(response, '83.0')
