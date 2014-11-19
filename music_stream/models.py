from django.db import models
from django.db.models import Model
from os.path import splitext

class Music(models.Model):
	name = models.CharField(max_length=128,unique=True)
	blue = 'hello'
	musicfile = models.FileField(upload_to='music/%Y/%m/%d')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = splitext(self.name)[0]
		super(Music,self).save(*args, **kwargs)

# Create your models here.
