import decimal

import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.utils.constants import TWOPLACES
from wger.weight.models import WeightEntry


class CompareUserDataTestCase(WorkoutManagerTestCase):
    '''
    Test the representation of a model
    '''
    USER_1 = {'first_name': 'Cletus',
              'last_name': 'Spuckle',
              'username': 'cletus',
              'email': 'cletus@testing.com',
              'role': 'admin'}

    USER_2 = {'first_name': 'John',
              'last_name': 'Speke',
              'username': 'speke',
              'email': 'speke@testing.com',
              'role': 'admin'}

    def add_user(self, data):
        '''
        Helper function to add users
        '''
        self.client.post(reverse('gym:gym:add-user', kwargs={'gym_pk': 1}), data)

        new_user = User.objects.get(pk=self.client.session['gym.user']['user_pk'])
        return new_user

    def add_weight(self, user_id, weight, date):
        '''
        Helper function to add weight to users
        '''
        WeightEntry.objects.create(
            weight=decimal.Decimal(weight).quantize(TWOPLACES),
            date=datetime.datetime.strptime(date, "%d%m%Y").date(),
            user=user_id
        )

    def test_multiple_weight_api_fail(self):
        self.user_login('admin')
        response = self.client.get(reverse('weight:multiple-weight-data',
                                           kwargs={'user_list': 'wrong_user'}))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', str(response.data))

    def test_multiple_weight_api(self):
        '''
        Test that the multiple weight api returns the correct values
        '''
        self.user_login('admin')
        user1 = self.add_user(self.USER_1)
        user2 = self.add_user(self.USER_2)
        self.add_weight(user1, 79.3, '05072017')
        self.add_weight(user1, 89.5, '07072017')
        self.add_weight(user2, 59.3, '05072017')
        self.add_weight(user2, 69.2, '07072017')

        response = self.client.get(reverse(
            'weight:multiple-weight-data',
            kwargs={'user_list': '{}-or-{}'.format(user1.username, user2.username)}
        ))
        response_str = str(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('79.3', response_str)
        self.assertIn('89.5', response_str)
        self.assertIn('59.3', response_str)
        self.assertIn('69.2', response_str)

        self.user_logout()

    def test_compare_weight(self):
        self.user_login('admin')
        user1 = self.add_user(self.USER_1)
        user2 = self.add_user(self.USER_2)
        self.add_weight(user1, 79.3, '05072017')
        self.add_weight(user1, 89.5, '07072017')
        self.add_weight(user2, 59.3, '05072017')
        self.add_weight(user2, 69.2, '07072017')

        response = self.client.get(reverse(
            'gym:gym:user-compare',
            kwargs={'pk': 1,
                    'user_list': '{}-or-{}'.format(user1.id, user2.id)}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user1.username)
        self.assertContains(response, user2.username)
        self.assertContains(response, 'Weight Details')
