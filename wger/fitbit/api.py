import os, base64, requests, urllib
import urllib.parse
from django.conf import settings
from requests.auth import HTTPBasicAuth

from wger.fitbit.models import TokenManager


class Fitbit():

    # All information must be as on the https://dev.fitbit.com/apps page.
    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET
    REDIRECT_URI = settings.REDIRECT_URI

    # Decide which information the FitBit.py should have access to.
    # Options: 'activity', 'heartrate', 'location', 'nutrition',
    #          'profile', 'settings', 'sleep', 'social', 'weight'
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
            'response_type':  'code',
            'scope': ' '.join(self.API_SCOPES),
            'redirect_uri': self.REDIRECT_URI
        }

        # Encode parameters and construct
        #  authorization url to be returned to user.
        urlparams = urllib.parse.urlencode(params)
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

        # Strip the goodies
        token = dict()
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        # Save token data to the database
        user_token = TokenManager(
            refresh_token=response['refresh_token'],
            access_token=response['access_token'],
            user=user,
            has_fitbit_integration=True
        )
        user_token.save()

        return token

    # Get new tokens based if authentication token is expired
    def ref_access_token(self, token):

        # Construct the authentication header
        auth_header\
            = base64.b64encode(self.CLIENT_ID + ':' + self.CLIENT_SECRET)
        headers = {
            'Authorization': 'Basic %s' % auth_header,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        # Set up parameters for refresh request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # Place request
        resp = requests.post(self.TOKEN_URL, data=params, headers=headers)

        status_code = resp.status_code
        resp = resp.json()

        if status_code != 200:
            raise Exception("Something went wrong refreshing (%s): %s"
                            % (resp['errors'][0]['errorType'],
                            resp['errors'][0]['message']))

        # Distil
        token['access_token'] = resp['access_token']
        token['refresh_token'] = resp['refresh_token']

        return token

    # Place api call to retrieve data
    def api_call(self, token,
                 api_call='/1/user/-/activities/log/steps/date/today/1d.json'):
        # (https://dev.fitbit.com/docs/), e.g.:
        # apiCall = '/1/user/-/devices.json'
        # apiCall = '/1/user/-/profile.json'
        # apiCall = '/1/user/-/activities/date/2015-10-22.json'

        headers = {
            'Authorization': 'Bearer %s' % token['access_token']
        }

        final_url = 'https://' + self.API_SERVER + api_call

        resp = requests.get(final_url, headers=headers)

        status_code = resp.status_code

        resp = resp.json()
        resp['token'] = token

        if status_code == 200:
            return resp
        elif status_code == 401:
            print("The access token you provided has been expired let me"
                  " refresh that for you.")
            # Refresh the access token with the refresh token if expired.
            #  Access tokens should be good for 1 hour.
            token = self.ref_access_token(token)
            self.api_call(token, api_call)
        else:
            raise Exception("Something went wrong requesting"
                            " (%s): %s" % (resp['errors'][0]['errorType'],
                                           resp['errors'][0]['message']))

    def string_to_base64(self, text):
        return base64.b64encode(text.encode('utf-8'))
