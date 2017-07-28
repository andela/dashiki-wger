# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    A command that gives a user access to create a user via API
    '''

    help = 'Give user permission to create users'

    def add_argument(self, parser):
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('app')

    def handle(self, *args, **options):
        # check if user exists
        user = User.object.filter(username=options["username"])
        if user:
            user.can_create_via_api = True

            user.save()
        else:
            return "Could not find user"
