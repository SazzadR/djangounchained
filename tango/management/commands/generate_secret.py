import re
import os

from django.core.management import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Set the application secret key'

    def add_arguments(self, parser):
        parser.add_argument(
            '--genesis',
            action='store_true',
            help='Bypass confirm dialogue',
        )

    def handle(self, *args, **options):
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))

        if Command.confirm(options):
            self.set_secret_key(env_path, get_random_secret_key())

    @staticmethod
    def confirm(options):
        if options['genesis']:
            pass
        else:
            print('This will overwrite your existing SECRET_KEY, want to proceed? (y/n)')
        try:
            answer = input() if not options['genesis'] else 'y'
            if answer == 'y' or answer == 'Y':
                return True
            return False
        except KeyboardInterrupt:
            return False

    @staticmethod
    def set_secret_key(env_file_path, secret_key):
        fp = open(env_file_path, 'r+')

        current_env = fp.read()
        regex = r"(SECRET_KEY=.*?)\n"

        matches = re.findall(regex, current_env)

        updated_env = current_env.replace(matches[0], 'SECRET_KEY={}'.format(secret_key))

        fp.seek(0)
        fp.truncate()
        fp.write(updated_env)

        fp.close()
