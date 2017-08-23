import csv
import sys

from os import path


from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from wger.core.models import UserProfile

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class ApiUserCommandsTestCase(TestCase):
    '''
     Test give user permission commands
    '''

    def test_add_user_rest_api(self):
        new_user = User.objects.create(username='Williams')
        new_user_profile = UserProfile.objects.get(user=new_user)

        self.assertFalse(new_user_profile.can_create_via_api)

        call_command('add-user-rest-api', 'Williams')
        new_user_profile.refresh_from_db()

        self.assertTrue(new_user_profile.can_create_via_api)

    def test_delete_user_rest_api(self):
        new_user = User.objects.create(username='Williams')
        new_user_profile = UserProfile.objects.get(user=new_user)

        new_user_profile.can_create_via_api = True
        new_user_profile.save()

        self.assertTrue(new_user_profile.can_create_via_api)

        call_command('delete-user-rest-api', 'Williams')

        new_user_profile.refresh_from_db()
        self.assertFalse(new_user_profile.can_create_via_api)

    def test_list_user_rest_api(self):
        new_user = User.objects.create(username='Williams')

        first_api_user = User.objects.create(username='Api Man')
        first_api_user_profile = UserProfile.objects.get(user=first_api_user)
        first_api_user_profile.app_flag = new_user.username
        first_api_user_profile.save()
        first_api_user_profile.refresh_from_db()

        second_api_user = User.objects.create(username='Another Api Man')
        second_api_user_profile = UserProfile.objects.get(user=second_api_user)
        second_api_user_profile.app_flag = new_user.username
        second_api_user_profile.save()
        second_api_user_profile.refresh_from_db()

        call_command(
            'list-user-rest-api', 'Williams')

        with open('wger/core/tests/test.txt') as f:
            data = f.readlines()
        reader = csv.reader(data)
        william_users = []
        for row in reader:
            william_users.append(row)
        self.assertIn('Another Api Man', william_users[1])
        self.assertIn('Api Man', william_users[0])
