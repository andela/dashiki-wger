import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from django.conf import settings
from requests.auth import HTTPBasicAuth

from wger.fitbit.models import TokenManager


class Fitbit():

    # All information must be as on the https://dev.fitbit.com/apps page.
    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET
    REDIRECT_URI = settings.REDIRECT_URI

    # Decide which information the FitBit.py should have access to.
    API_SCOPES = ('activity', 'heartrate', 'location', 'nutrition', 'profile',
                  'settings', 'sleep', 'social', 'weight')

    # These settings should probably not be changed.
    API_SERVER = 'api.fitbit.com'
    WWW_SERVER = 'www.fitbit.com'
    AUTHORIZE_URL = 'https://%s/oauth2/authorize' % WWW_SERVER
    TOKEN_URL = 'https://%s/oauth2/token' % API_SERVER

    def get_authorization_uri(self):

        # Parameters for authorization, make sure to select
        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': ' '.join(self.API_SCOPES),
            'redirect_uri': self.REDIRECT_URI
        }

        # Encode parameters and construct
        #  authorization url to be returned to user.
        urlparams = urlencode(params)
        return "%s?%s" % (self.AUTHORIZE_URL, urlparams)

    # Tokes are requested based on access code.
    # Access code must be fresh (10 minutes)
    def get_access_token(self, access_code, user):

        params = {
            'code': access_code,
            'grant_type': 'authorization_code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI
        }

        # Place request
        response = requests.post(
            self.TOKEN_URL, auth=HTTPBasicAuth(
                self.CLIENT_ID, self.CLIENT_SECRET), data=params)

        status_code = response.status_code
        response = response.json()

        if status_code != 200:
            raise Exception("Something went wrong exchanging code for"
                            " token (%s): %s" %
                            (response['errors'][0]['errorType'],
                             response['errors'][0]['message']))

        user_token = user.tokenmanager
        if not user_token:
            # Save token data to the database
            user_token = TokenManager(
                refresh_token=response['refresh_token'],
                access_token=response['access_token'],
                user=user,
                has_fitbit_integration=True
            )
            user_token.save()
            return

        user_token.refresh_token = response['refresh_token']
        user_token.access_token = response['access_token']
        user_token.save()

    # Get new tokens based if authentication token is expired
    def ref_access_token(self, token):

        # Set up parameters for refresh request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token.refresh_token
        }

        # Place request
        response = requests.post(
            self.TOKEN_URL, auth=HTTPBasicAuth(
                self.CLIENT_ID, self.CLIENT_SECRET), data=params)

        status_code = response.status_code
        response = response.json()

        if status_code != 200:
            raise Exception("Something went wrong refreshing (%s): %s"
                            % (response['errors'][0]['errorType'],
                               response['errors'][0]['message']))

        token.access_token = response['access_token']
        token.refresh_token = response['refresh_token']
        token.save()

        return token

    # Place api call to retrieve data
    def api_call(self, token, api_call):

        headers = {
            'Authorization': 'Bearer %s' % token.access_token
        }

        final_url = 'https://' + self.API_SERVER + api_call

        response = requests.get(final_url, headers=headers)

        status_code = response.status_code

        response = response.json()

        if status_code == 200:
            return response
        elif status_code == 401:
            print("The access token you provided has been expired let me"
                  " refresh that for you.")
            # Refresh the access token with the refresh token if expired.
            #  Access tokens should be good for 1 hour.
            self.ref_access_token(token)
            self.api_call(token, api_call)

        else:
            raise Exception("Something went wrong requesting"
                            " (%s): %s" % (response['errors'][0]['errorType'],
                                           response['errors'][0]['message']))
