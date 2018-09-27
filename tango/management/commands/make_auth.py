import os
import re
from django.conf import settings
from tango.helpers.utils import with_default
from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Scaffold basic login and registration views and routes'

    def __init__(self):
        super().__init__()

        self.app_name = 'accounts'

        print('Do you want to use custom User model? (y/n): ', end='')
        model_input = input().lower()
        self.custom_user_model = with_default((model_input == 'y'), False)

        self.settings_file = '{}/{}/settings.py'.format(settings.BASE_DIR, os.getenv('APP_NAME'))
        self.views = {
            'tango/stubs/accounts/views/default/forms.stub': '{0}/forms.py'.format(
                self.app_name),
            'tango/stubs/accounts/views/default/login.stub': '{0}/views/login.py'.format(
                self.app_name),
            'tango/stubs/accounts/views/default/register.stub': '{0}/views/register.py'.format(
                self.app_name)
        }
        self.templates = {
            'tango/stubs/accounts/templates/app.stub': 'templates/{0}/layouts/app.html'.format(os.getenv('APP_NAME')),
            'tango/stubs/accounts/templates/default/login.stub': '{0}/templates/{0}/login.html'.format(
                self.app_name),
            'tango/stubs/accounts/templates/default/register.stub': '{0}/templates/{0}/register.html'.format(
                self.app_name)
        }

    def handle(self, *args, **options):
        self.create_app()
        self.create_models_and_backend()
        self.update_settings()
        self.scaffold_actions()

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
        backend_file_path = 'tango/stubs/accounts/authentication_backends/backend_default.stub'
        with open(backend_file_path, 'r') as fp:
            stub = fp.read()
            return stub

    def scaffold_actions(self):
        self.create_views()
        self.create_templates()
        self.create_urls()
        self.update_homepage()

    def create_views(self):
        os.makedirs(self.app_name + '/views', exist_ok=True)
        with open(self.app_name + '/views/__init__.py', 'w') as fp:
            pass
        fp.close()

        for stub in self.views:
            view_name = self.views[stub]
            os.makedirs(os.path.dirname(view_name), exist_ok=True)
            with open(view_name, 'w') as fp:
                with open(stub, 'r') as fp_stub:
                    fp.write(fp_stub.read().replace('{app_name}', self.app_name))
                fp_stub.close()
            fp.close()

    def create_templates(self):
        for stub in self.templates:
            template_name = self.templates[stub]

            os.makedirs(os.path.dirname(template_name), exist_ok=True)
            with open(template_name, 'w') as fp:
                with open(stub, 'r') as fp_stub:
                    fp.write(fp_stub.read().replace('{project_name}', os.getenv('APP_NAME')))
                fp_stub.close()
            fp.close()

    def create_urls(self):
        with open('{}/urls.py'.format(self.app_name), 'w') as fp:
            with open('tango/stubs/accounts/urls.stub', 'r') as fp_stub:
                stub = fp_stub.read().replace('{app_name}', self.app_name)
                fp.write(stub)
            fp_stub.close()
        fp.close()

        with open(os.getenv('APP_NAME') + '/urls.py', 'r') as fp:
            current_urls_file_content = fp.read()
        fp.close()

        updated_url_file = current_urls_file_content.replace("urlpatterns = [\n",
                                                             "urlpatterns = [\n    path('', include('{}.urls', namespace='accounts')),\n".format(
                                                                 self.app_name))

        with open(os.getenv('APP_NAME') + '/urls.py', 'w') as fp:
            fp.write(updated_url_file)
        fp.close()

    def update_homepage(self):
        default_template = 'templates/' + os.getenv('APP_NAME') + '/default.html'

        with open(default_template, 'r') as fp:
            updated_contents = fp.read() \
                .replace('<a href="javascript:void(0)">Login</a>', '<a href="{% url \'accounts:login\' %}">Login</a>') \
                .replace('<a href="javascript:void(0)">Register</a>',
                         '<a href="{% url \'accounts:register\' %}">Register</a>')
        fp.close()

        with open(default_template, 'w') as fp:
            fp.write(updated_contents)
        fp.close()
