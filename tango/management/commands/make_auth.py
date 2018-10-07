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

        self.accounts_app_name = 'accounts'
        self.home_app_name = 'home'

        print('Do you want to use custom User model? (y/n): ', end='')
        model_input = input().lower()
        self.custom_user_model = with_default((model_input == 'y'), False)

        self.settings_file = '{}/{}/settings.py'.format(settings.BASE_DIR, os.getenv('APP_NAME'))
        self.accounts_views = {
            'tango/stubs/accounts/views/default/forms.stub': '{0}/forms.py'.format(
                self.accounts_app_name),
            'tango/stubs/accounts/views/default/login.stub': '{0}/views/login.py'.format(
                self.accounts_app_name),
            'tango/stubs/accounts/views/default/register.stub': '{0}/views/register.py'.format(
                self.accounts_app_name)
        }
        self.accounts_templates = {
            'tango/stubs/accounts/templates/app.stub': 'templates/{0}/layouts/app.html'.format(os.getenv('APP_NAME')),
            'tango/stubs/accounts/templates/default/login.stub': '{0}/templates/{0}/login.html'.format(
                self.accounts_app_name),
            'tango/stubs/accounts/templates/default/register.stub': '{0}/templates/{0}/register.html'.format(
                self.accounts_app_name)
        }
        self.home_templates = {
            'tango/stubs/home/templates/home.stub': '{0}/templates/{0}/home.html'.format(
                self.home_app_name)
        }

    def handle(self, *args, **options):
        # self.create_accounts_app()
        self.create_home_app()

    def create_accounts_app(self):
        self.create_app(self.accounts_app_name)
        self.create_models_and_backend()
        self.update_settings()
        self.scaffold_actions()

    def create_home_app(self):
        self.create_app(self.home_app_name)
        self.update_installed_app(self.home_app_name)
        self.create_templates(self.home_templates)
        self.create_urls(self.home_app_name, 'home')

    def create_app(self, name):
        if os.path.exists(name):
            raise ValueError('{} app or directory already exists!'.format(name))

        call_command('startapp', name)

    def update_installed_app(self, app_name):
        with open(self.settings_file, 'r') as fp:
            file_contents = fp.read()
            fp.close()

        # Update INSTALLED_APPS
        file_contents = re.sub(r"('tango',)", r"\1\n    '{}',".format(app_name), file_contents)

        with open(self.settings_file, 'w') as fp:
            fp.write(file_contents)
            fp.close()

    def create_models_and_backend(self):
        if self.custom_user_model:
            pass
        else:
            self.create_default_model()

    def create_default_model(self):
        model_file_path = self.accounts_app_name + '/models.py'

        with open(model_file_path, 'w') as fp:
            stub = self.load_model_stub('default')
            fp.write(stub)

    def update_settings(self):
        with open(self.settings_file, 'r') as fp:
            file_contents = fp.read()
            fp.close()

        # Update INSTALLED_APPS
        file_contents = re.sub(r"('tango',)", r"\1\n    '{}',".format(self.accounts_app_name), file_contents)

        # Add AUTH_USER_MODEL
        file_contents += "\n\n# User model\nAUTH_USER_MODEL = '{}.User'\n\n\n".format(self.accounts_app_name)

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
        self.create_templates(self.accounts_templates)
        self.create_urls(self.accounts_app_name)
        self.update_homepage()

    def create_views(self):
        os.makedirs(self.accounts_app_name + '/views', exist_ok=True)
        with open(self.accounts_app_name + '/views/__init__.py', 'w') as fp:
            pass
        fp.close()

        for stub in self.accounts_views:
            view_name = self.accounts_views[stub]
            os.makedirs(os.path.dirname(view_name), exist_ok=True)
            with open(view_name, 'w') as fp:
                with open(stub, 'r') as fp_stub:
                    fp.write(fp_stub.read().replace('{app_name}', self.accounts_app_name))
                fp_stub.close()
            fp.close()

    def create_templates(self, templates):
        for stub in templates:
            template_name = templates[stub]

            os.makedirs(os.path.dirname(template_name), exist_ok=True)
            with open(template_name, 'w') as fp:
                with open(stub, 'r') as fp_stub:
                    fp.write(fp_stub.read().replace('{project_name}', os.getenv('APP_NAME')))
                fp_stub.close()
            fp.close()

    def create_urls(self, app_name, namespace=''):
        with open('{}/urls.py'.format(app_name), 'w') as fp:
            with open('tango/stubs/{}/urls.stub'.format(app_name), 'r') as fp_stub:
                stub = fp_stub.read().replace('{app_name}', app_name)
                fp.write(stub)
            fp_stub.close()
        fp.close()

        with open(os.getenv('APP_NAME') + '/urls.py', 'r') as fp:
            current_urls_file_content = fp.read()
        fp.close()

        updated_url_file = current_urls_file_content.replace("urlpatterns = [\n",
                                                             "urlpatterns = [\n    path('{0}', include('{1}.urls', namespace='{1}')),\n"
                                                             .format(namespace, app_name))

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
