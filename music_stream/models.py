from django.db import models
from django.db.models import Model

class Music(models.Model):
	name = models.CharField(max_length=128,unique=True)
	musicfile = models.FileField(upload_to='music/%Y/%m/%d')

	def __unicode__(self):
		return self.name
# Create your models here.
