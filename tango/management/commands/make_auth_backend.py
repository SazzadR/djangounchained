import os

from django.core.management import call_command
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create custom backend for auth'

    def __init__(self):
        super().__init__()
        self.app_name = None

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, nargs='?', default='tango_authentication')

    def handle(self, *args, **options):
        self.app_name = options['app_name']

        self.create_app()
        self.create_backend()

    def create_app(self):
        if os.path.exists(self.app_name):
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
