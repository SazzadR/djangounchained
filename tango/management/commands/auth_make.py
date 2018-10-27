import os
import re
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import call_command
from tango.support.file_system import FileSystem, FileContents, StringContents


class Command(BaseCommand):
    help = 'Scaffold basic login and registration views and routes'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)

        self.file_system = FileSystem()

        self.settings_file = '{}/{}/settings.py'.format(settings.BASE_DIR, os.getenv('APP_NAME'))

        self.accounts_app_name = 'accounts'
        self.home_app_name = 'home'

        self.accounts_templates = {
            'tango/stubs/accounts/templates/app.stub': 'templates/{0}/layouts/app.html'.format(os.getenv('APP_NAME')),
            'tango/stubs/accounts/templates/default/login.stub': '{0}/templates/{0}/login.html'.format(
                self.accounts_app_name),
            'tango/stubs/accounts/templates/default/register.stub': '{0}/templates/{0}/register.html'.format(
                self.accounts_app_name)
        }
        self.home_templates = {
            'tango/stubs/home/templates/home.stub': '{0}/templates/{0}/home.html'.format(self.home_app_name)
        }

        self.accounts_models = {
            'tango/stubs/accounts/models/model_default.stub': '{0}/models.py'.format(self.accounts_app_name),
        }

        self.accounts_forms = {
            'tango/stubs/accounts/views/default/forms.stub': '{0}/forms.py'.format(self.accounts_app_name),
        }

        self.accounts_views = {
            'tango/stubs/miscellaneous/__init__.stub': '{0}/views/__init__.py'.format(self.accounts_app_name),
            'tango/stubs/accounts/views/default/login.stub': '{0}/views/login.py'.format(self.accounts_app_name),
            'tango/stubs/accounts/views/default/register.stub': '{0}/views/register.py'.format(self.accounts_app_name)
        }
        self.home_views = {
            'tango/stubs/home/views.stub': '{0}/views.py'.format(self.home_app_name)
        }

        self.accounts_urls = {
            'tango/stubs/accounts/urls.stub': '{0}/urls.py'.format(self.accounts_app_name),
        }
        self.home_urls = {
            'tango/stubs/home/urls.stub': '{0}/urls.py'.format(self.home_app_name),
        }

        self.default_template = {
            'templates/{0}/default.html'.format(os.getenv('APP_NAME')):
                'templates/{0}/default.html'.format(os.getenv('APP_NAME'))
        }

    def handle(self, *args, **options):
        self.create_app(self.accounts_app_name)
        self.create_templates(self.accounts_templates)
        self.create_models(self.accounts_models)
        self.create_forms(self.accounts_forms, {
            '{app_name}': os.getenv('APP_NAME')
        })
        self.create_views(self.accounts_views, {
            '{app_name}': self.accounts_app_name
        })
        self.create_urls(self.accounts_urls, {
            '{app_name}': self.accounts_app_name
        })
        self.register_app(self.accounts_app_name)
        self.update_auth_model()
        self.add_authentication_backends()

        self.create_app(self.home_app_name)
        self.create_templates(self.home_templates)
        self.create_views(self.home_views, {
            '{app_name}': self.home_app_name
        })
        self.create_urls(self.home_urls, {
            '{app_name}': self.home_app_name
        })
        self.register_app(self.home_app_name)

        self.update_default_template(self.default_template, {
            '<a href="javascript:void(0)">Login</a>':
                '<a href="{% url \'accounts:login\' %}">Login</a>',
            '<a href="javascript:void(0)">Register</a>':
                '<a href="{% url \'accounts:register\' %}">Register</a>',
            '<a href="javascript:void(0)">Home</a>':
                '<a href="{% url \'home:index\' %}">Home</a>'
        })

        self.update_system_urls(self.accounts_app_name)
        self.update_system_urls(self.home_app_name, 'home')

    def create_app(self, app_name):
        if os.path.exists(app_name):
            raise ValueError('{} app or directory already exists!'.format(app_name))

        call_command('startapp', app_name)

    def create_templates(self, templates):
        for stub in templates:
            source = FileContents(stub)
            self.file_system.create_from_stub(
                source=source,
                destination=templates[stub],
                replace={
                    '{project_name}': os.getenv('APP_NAME')
                }
            )

    def create_models(self, models):
        for stub in models:
            source = FileContents(stub)
            self.file_system.create_from_stub(
                source=source,
                destination=models[stub]
            )

    def create_forms(self, forms, replace):
        for stub in forms:
            source = FileContents(stub)
            self.file_system.create_from_stub(
                source=source,
                destination=forms[stub],
                replace=replace
            )

    def create_views(self, views, replace):
        for stub in views:
            source = FileContents(stub)
            self.file_system.create_from_stub(
                source=source,
                destination=views[stub],
                replace=replace
            )

    def create_urls(self, urls, replace):
        for stub in urls:
            source = FileContents(stub)
            self.file_system.create_from_stub(
                source=source,
                destination=urls[stub],
                replace=replace
            )

    def register_app(self, app_name):
        with open(self.settings_file, 'r') as fp:
            settings_file_contents = fp.read()
        fp.close()

        source = StringContents(settings_file_contents)

        self.file_system.create_from_stub(
            source=source,
            destination=self.settings_file,
            replace={
                settings_file_contents:
                    re.sub(r"('tango',)", r"\1\n    '{}',".format(app_name), settings_file_contents)
            }
        )

    def update_auth_model(self):
        with open(self.settings_file, 'r') as fp:
            settings_file_contents = fp.read()
        fp.close()

        source = StringContents(settings_file_contents)

        updated_settings_file_contents = settings_file_contents
        updated_settings_file_contents += \
            "\n\n# User model\nAUTH_USER_MODEL = '{}.User'\n\n\n".format(self.accounts_app_name)

        self.file_system.create_from_stub(
            source=source,
            destination=self.settings_file,
            replace={
                settings_file_contents: updated_settings_file_contents
            }
        )

    def add_authentication_backends(self):
        with open(self.settings_file, 'r') as fp:
            settings_file_contents = fp.read()
        fp.close()

        source = StringContents(settings_file_contents)

        backend_stub = FileContents('tango/stubs/accounts/authentication_backends/backend_default.stub')

        updated_settings_file_contents = settings_file_contents
        updated_settings_file_contents += backend_stub.get_contents()

        self.file_system.create_from_stub(
            source=source,
            destination=self.settings_file,
            replace={
                settings_file_contents: updated_settings_file_contents
            }
        )

    def update_default_template(self, default_template, replace):
        for stub in default_template:
            with open(stub, 'r') as fp:
                template_file_contents = fp.read()
            fp.close()

            source = StringContents(template_file_contents)

            self.file_system.create_from_stub(
                source=source,
                destination=default_template[stub],
                replace=replace
            )

    def update_system_urls(self, app_name, namespace=''):
        with open(os.getenv('APP_NAME') + '/urls.py', 'r') as fp:
            current_urls_file_content = fp.read()
        fp.close()

        updated_url_file_content = current_urls_file_content. \
            replace("urlpatterns = [\n",
                    "urlpatterns = [\n    path('{0}', include('{1}.urls', namespace='{1}')),\n"
                    .format(namespace, app_name))

        with open(os.getenv('APP_NAME') + '/urls.py', 'w') as fp:
            fp.write(updated_url_file_content)
        fp.close()
