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

    def add_user(self, data):
        '''
        Helper function to add users
        '''

        response = self.client.post(reverse('gym:gym:add-user', kwargs={'gym_pk': 1}), data)

        new_user = User.objects.get(pk=self.client.session['gym.user']['user_pk'])
        return new_user

    def add_weight(self, user_id):
        response = WeightEntry.objects.create(
            weight=decimal.Decimal(81.1).quantize(TWOPLACES),
            date=datetime.date(2013, 2, 1),
            user=user_id
        )

    def test_select_members(self):
        '''
        Test that the representation of an object is correct
        '''
        self.user_login('admin')
        user1 = self.advd_user({
            'first_name': 'Cletus',
            'last_name': 'Spuckle',
            'username': 'cletus',
            'email': 'cletus@testing.com',
            'role': 'admin'})
        self.add_weight(user1)

        # user2 = self.add_user({
        #     'first_name': 'John',
        #     'last_name': 'Speke',
        #     'username': 'speke',
        #     'email': 'speke@testing.com',
        #     'role': 'admin'})

