import django
import csv
#from django.core.management import setup_environ
from coursematch import settings
#setup_environ(settings)
import sys,os
from django.core.wsgi import get_wsgi_application
#sys.path.append()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursematch.settings")
django.setup()
application = get_wsgi_application()
from course.models import *
with open("data.csv") as f:
       reader = csv.reader(f,delimiter=',')
       rows = list(reader)
       for row in range(10):
           _, created = CourseModel.objects.get_or_create(
               title = rows[row][0],
               homepage = rows[row][1],
               image = rows[row][2],
               short_summary = rows[row][3],
               summary = rows[row][4]
               )
