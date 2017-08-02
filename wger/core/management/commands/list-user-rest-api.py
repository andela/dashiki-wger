import sys
from django.core.management.base import BaseCommand
from wger.core.models import UserProfile
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Command(BaseCommand):
    '''
    A command that lists all users created via the api by a specific app
    '''

    help = 'List all users created by app'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)
        parser.add_argument('filename', nargs='?', type=str)

    def handle(self, *args, **options):
        # check if user exists
        username = options.get('username', None)
        filename = options.get('filename', None)

        users = UserProfile.objects.all().filter(app_flag=username)
        if users:

            orig_stdout = sys.stdout
            if not filename:
                filename = 'test.txt'
                saveFile = open('wger/core/tests/' + filename, 'w')
                sys.stdout = saveFile
            else:
                saveFile = open(filename, 'w')
                sys.stdout = saveFile

            for user in users:
                print(user.user.username)

            sys.stdout = orig_stdout
            saveFile.close()
            return 'Successfully printed out users created by {}'.format(
                username)

        else:
            return 'No users created by {}'.format(username)
