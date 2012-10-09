from django.db import models
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
import datetime


class Choice(models.Model):
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
      return self.choice

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    choices = ListField(EmbeddedModelField('Choice'))
    
    def __unicode__(self):
      return self.question

    def was_published_today(self):
      return self.pub_date.date() == datetime.date.today()
