from django.db import models
from django.db.models import Model

class Music(models.Model):
	musicfile = models.FileField(upload_to='music/%Y/%m/%d')
# Create your models here.
