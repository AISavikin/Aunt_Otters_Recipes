import os
from datetime import date


os.system(f'python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db_{date.today()}.json')