from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import URLValidator
# Create your models here.
from elasticsearchapp.search import CourseModelIndex


class CourseModel(models.Model):
    title = models.CharField(max_length=100)
    homepage = models.CharField(max_length = 120)
    image = models.CharField(max_length=120)
    short_summary = models.CharField(max_length = 200)
    summary = models.CharField(max_length = 400)

    def __str__(self):
        return "{0}".format(self.title)

class CoursereviewModel(models.Model):
    rating = models.IntegerField()
    review = models.CharField(max_length = 200)
    course = models.ForeignKey(CourseModel,null = True,blank = True)
    user = models.ForeignKey(User,default = 'moorthy')
    def __str__(self):
        return "{0}".format(self.user)
def indexing(self):
   obj = CourseModelIndex(
      meta={'id': self.id},
      title=self.author.title,
      short_summary=self.short_summary,
      summary=self.summary
   )
   obj.save()
   return obj.to_dict(include_meta=True)
