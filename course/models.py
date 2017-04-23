from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import URLValidator
# Create your models here.
class CourseModel(models.Model):
    title = models.CharField(max_length=100)
    homepage = models.CharField(max_length = 120)
    image = models.CharField(max_length=120)
    short_summary = models.CharField(max_length = 200)
    summary = models.CharField(max_length = 400)

    def __str__(self):
        return "{0}".format(self.title)

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    course = models.ManyToManyField(CourseModel,null = True,blank = True)
    def __str__(self):
        return "{0}".format(self.user)
