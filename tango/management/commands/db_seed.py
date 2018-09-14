import os
import ast
import importlib.machinery
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Seed the database with records'

    def handle(self, *args, **options):
        self.run_seeds()

    @staticmethod
    def run_seeds():
        app_name = os.getenv('APP_NAME') + '.database_seeder'
        module = importlib.import_module(app_name)
        database_seeder_class = getattr(module, 'DatabaseSeeder')

        for seed in database_seeder_class.seeds:
            class_name = Command.get_seed_class_name(seed.__file__)
            seed_module = importlib.machinery.SourceFileLoader('seed', seed.__file__).load_module()
            seed_class = getattr(seed_module, class_name)
            seed_class.run()

    @staticmethod
    def get_seed_class_name(seed_file):
        fp = open(seed_file, 'r')
        p = ast.parse(fp.read())
        classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        fp.close()

        return classes[0]
