from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    A command that lists all users created via the api by a specific app
    '''

    help = 'List all users created by app'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)

    def handle(self, *args, **options):
        # check if user exists
        username = options.get('username', None)
        try:

            users = UserProfile.objects.all().filter(api_flag=username)

            for user in users:
                print(user.user.username)

        except:
            return "There are no users created by {}".format(username)
