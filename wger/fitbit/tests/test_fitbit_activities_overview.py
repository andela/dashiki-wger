import mock
from django.core.urlresolvers import reverse
from mock import patch
from django.contrib.auth.models import User

from wger.fitbit.api import Fitbit
from wger.fitbit.models import TokenManager
from django.conf import settings
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class FitbitActivitiesTestCase(WorkoutManagerTestCase):
    SITE_URL = settings.SITE_URL
    fitbit = Fitbit()
    user = User.objects.get(pk=1)

    @patch('wger.fitbit.api.requests.get')
    def test_fitbit_activities_overview(self, mock_api_call):
        # authorize_token_url calls oauth and returns a URL
        self.user_login()
        mock_response = mock.Mock()
        expected_dict = \
            {
                "activities": [
                    {
                        "activityId": 51007,
                        "activityParentId": 90019,
                        "calories": 230,
                        "description": "7mph",
                        "distance": 2.04,
                        "duration": 1097053,
                        "name": "Treadmill, 0% Incline",
                        "startTime": "00:25",
                        "steps": 3783
                    }
                ]
            }
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_api_call.return_value = mock_response

        user_token = TokenManager(
            refresh_token='refresh_token',
            access_token='access_token',
            user=self.user,
            has_fitbit_integration=True
        )
        user_token.save()
        response = self.client.get(
            self.SITE_URL + reverse('fitbit:activities'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities.html')
        self.assertContains(response, 'Treadmill')
