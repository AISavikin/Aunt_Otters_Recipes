import os

os.system('python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db_test.json')