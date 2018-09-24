import os
import re
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Scaffold basic login and registration views and routes'

    def __init__(self):
        super().__init__()
        self._app_name = 'accounts'
        self._custom_user_model = False
        self.settings_file = '{}/{}/settings.py'.format(settings.BASE_DIR, os.getenv('APP_NAME'))

    @property
    def app_name(self):
        return self._app_name

    @property
    def custom_user_model(self):
        return self._custom_user_model

    @app_name.setter
    def app_name(self, value):
        if len(value) > 0:
            self._app_name = value
        else:
            self._app_name = 'accounts'

    @custom_user_model.setter
    def custom_user_model(self, value):
        self._custom_user_model = True if value.lower() == 'y' else False

    def handle(self, *args, **options):
        self.receive_parameters()
        self.create_app()
        self.create_models_and_backend()
        self.update_settings()

    def receive_parameters(self):
        print('App name(accounts): ', end='')
        self.app_name = input()

        print('Do you want to use custom User model? (y/n): ', end='')
        self.custom_user_model = input()

    def create_app(self):
        if os.path.exists(self.app_name) or ('AUTH_USER_MODEL' in open(self.settings_file).read()):
            raise ValueError('App or directory already exists!')

        call_command('startapp', self.app_name)

    def create_models_and_backend(self):
        if self.custom_user_model:
            pass
        else:
            self.create_default_model()

    def create_default_model(self):
        model_file_path = self.app_name + '/models.py'

        with open(model_file_path, 'w') as fp:
            stub = self.load_model_stub('default')
            fp.write(stub)

    def update_settings(self):
        with open(self.settings_file, 'r') as fp:
            file_contents = fp.read()
            fp.close()

        # Update INSTALLED_APPS
        file_contents = re.sub(r"('tango',)", r"\1\n    '{}',".format(self.app_name), file_contents)

        # Add AUTH_USER_MODEL
        file_contents += "\n\n# User model\nAUTH_USER_MODEL = '{}.User'\n\n\n".format(self.app_name)

        # Add AUTHENTICATION_BACKENDS
        file_contents += self.add_authentication_backends()

        with open(self.settings_file, 'w') as fp:
            fp.write(file_contents)
            fp.close()

    def load_model_stub(self, model_type):
        with open('tango/stubs/accounts/models/model_{}.stub'.format(model_type)) as fp:
            stub = fp.read()
            return stub

    def add_authentication_backends(self):
        if self.custom_user_model:
            backend_file_path = None
        else:
            backend_file_path = 'tango/stubs/accounts/authentication_backends/backend_default.stub'

        with open(backend_file_path, 'r') as fp:
            stub = fp.read()
            return stub
