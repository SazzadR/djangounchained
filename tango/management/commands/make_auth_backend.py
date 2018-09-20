import os
import re

from django.conf import settings
from django.core.management import call_command
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create custom backend for auth'

    def __init__(self):
        super().__init__()
        self.app_name = None
        self.settings_file = '{}/{}/settings.py'.format(settings.BASE_DIR, os.getenv('APP_NAME'))

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, nargs='?', default='tango_authentication')

    def handle(self, *args, **options):
        self.app_name = options['app_name']

        self.create_app()
        self.create_backend()
        self.update_settings()

    def create_app(self):
        if os.path.exists(self.app_name) or ('AUTH_USER_MODEL' in open(self.settings_file).read()):
            raise ValueError('App or directory already exists!')

        call_command('startapp', self.app_name)

    def load_stub(self):
        with open('tango/stubs/make_auth_backend.stub') as fp:
            stub = fp.read()
            return stub

    def create_backend(self):
        model_file_path = self.app_name + '/models.py'

        with open(model_file_path, 'w') as fp:
            stub = self.load_stub()
            fp.write(stub)

    def update_settings(self):
        with open(self.settings_file, 'r') as fp:
            file_contents = fp.read()
            fp.close()

        # Update installed apps
        file_contents = re.sub(r"('tango',)", r"\1\n    '{}',".format(self.app_name), file_contents)

        # Add custom user model
        file_contents += "\n\n# Custom User model\nAUTH_USER_MODEL = '{}.User'\n".format(self.app_name)

        with open(self.settings_file, 'w') as fp:
            fp.write(file_contents)
            fp.close()
