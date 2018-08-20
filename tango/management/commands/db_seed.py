import ast
import os
import glob
import importlib.machinery

from djangonautic import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Seed the database with records'

    def handle(self, *args, **options):
        apps = self.get_installed_apps()
        self.run_seeds(apps)

    @staticmethod
    def get_installed_apps():
        apps = []

        for app in settings.INSTALLED_APPS:
            if 'django.contrib' not in app:
                apps.append(app)

        return apps

    @staticmethod
    def run_seeds(apps):
        for app in apps:
            if os.path.isdir(app) and os.path.isdir(app + '/seeds'):
                for seed_file in glob.glob(app + '/seeds/[!_]*.py'):
                    class_name = Command.get_seed_class_name(seed_file)
                    seed_module = importlib.machinery.SourceFileLoader('seed', seed_file).load_module()
                    seed_class = getattr(seed_module, class_name)
                    seed_class.run()

    @staticmethod
    def get_seed_class_name(seed_file):
        fp = open(seed_file, 'r')
        p = ast.parse(fp.read())
        classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        fp.close()

        return classes[0]
