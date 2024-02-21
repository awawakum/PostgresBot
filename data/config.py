import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

PROJECT_NAME = 'ZaimBot'

IP = str(os.getenv('IP'))
POSTGRESQL_USER = str(os.getenv('POSTGRESQL_USER'))
POSTGRESQL_PASSWORD = str(os.getenv('POSTGRESQL_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
SQL_PORT =str(os.getenv('SQL_PORT'))

POSTGRES_URI = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{IP}:5432/cashsupport'

ADMINS = [5559290785, 1188427407]
