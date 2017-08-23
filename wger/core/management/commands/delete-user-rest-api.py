from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    A command that gives a user access to create a user via API
    '''

    help = 'Give user permission to create users'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)

    def handle(self, *args, **options):
        # check if user exists
        username = options.get('username', None)
        try:
            user = User.objects.get(username=username)

            profile = UserProfile.objects.get(user=user)
            if profile.can_create_via_api:
                profile.can_create_via_api = False
                profile.save()
                return '{} no longer has permission to create users'.format(username)
            else:
                return 'No action, {} does not have permission to create users'.format(username)
        except:
            return "Could not find user- {}".format(username)
