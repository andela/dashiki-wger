try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from wger.fitbit.api import Fitbit
from django.conf import settings

from wger.core.tests.base_testcase import WorkoutManagerTestCase


class FitbitAuthenticationTestCase(WorkoutManagerTestCase):
    client_kwargs = {
        'client_id': 'fake_id',
        'client_secret': 'fake_secret',
        'redirect_uri': 'http://127.0.0.1:8080',
        'scope': ['fake_scope1']
    }
    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET
    REDIRECT_URI = settings.REDIRECT_URI
    API_SCOPES = ('activity', 'heartrate', 'location', 'nutrition', 'profile',
                  'settings', 'sleep', 'social', 'weight')
    fitbit = Fitbit()

    def test_authorize_token_url(self):
        # authorize_token_url calls oauth and returns a URL
        response = self.fitbit.get_authorization_uri()
        params = urlencode({
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': ' '.join(self.API_SCOPES),
            'redirect_uri': self.REDIRECT_URI
        })
        expected_url = "https://www.fitbit.com/oauth2/authorize?%s" % params
        self.assertEqual(response, expected_url)
