import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, 'pycards/data.json')

FIXTURES_PATH = os.path.join(BASE_DIR, 'tests/fixtures.json')
