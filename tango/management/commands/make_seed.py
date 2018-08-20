import os
import re

from django.core.management import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.terminal_red_bg = '\33[41m'
        self.terminal_end = '\033[0m'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('seed_name', type=str)

    def handle(self, *args, **options):
        app_name = options['app_name']
        seed_name = options['seed_name']

        self.create_seed_file(app_name, seed_name)

    def create_seed_file(self, app_name, seed_name):
        seed_file_path = app_name + '/seeds/{}'.format(seed_name) + '.py'
        init_file_path = app_name + '/seeds/__init__.py'

        if not os.path.isfile(seed_file_path):
            if not os.path.isdir(os.path.dirname(seed_file_path)):
                os.makedirs(os.path.dirname(seed_file_path))
                with open(init_file_path, 'w') as fp:
                    fp.close()

            with open(seed_file_path, 'w') as fp:
                seed_stub = self.load_stub(seed_name)
                fp.write(seed_stub)
        else:
            print(self.terminal_red_bg + 'Seed already exists' + self.terminal_end)

    def load_stub(self, seed_name):
        with open('tango/stubs/make_seed.stub') as fp:
            class_stub = fp.read()

            regex = r"class (.*):"
            matches = re.findall(regex, class_stub)
            class_stub = class_stub.replace(matches[0], '{}'.format(self.underscore_to_camelcase(seed_name)))

            return class_stub

    def underscore_to_camelcase(self, text):
        return ''.join(x.capitalize() or '_' for x in text.split('_'))
