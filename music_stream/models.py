from django.db import models
from django.db.models import Model
from django.core.files.storage import FileSystemStorage
from os.path import splitext
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM
import hashlib

class CustomStorage(FileSystemStorage):
	def get_available_name(self, file_name):
		return file_name

	def _save(self, file_name, content):
		if self.exists(file_name):
			#if the file exists, do not save the new file
			return file_name
		#if the file does not exist, save the file
		return super(CustomStorage, self)._save(file_name, content)		

class Music(models.Model):
	name = models.CharField(max_length=128,unique=True)
	blue = 'hello'
	musicfile = models.FileField(upload_to='music/%Y/%m/%d')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = splitext(self.name)[0]
		super(Music,self).save(*args, **kwargs)


class Song(models.Model):
	owner = models.CharField(max_length=30,default=None)
	file_name = models.CharField(max_length=128)
	songfile = models.FileField(upload_to='music/%Y/%m/%d',storage=CustomStorage())
	md5sum = models.CharField(max_length=36)
	title = models.CharField(max_length=128,default='untitled')
	artist = models.CharField(max_length=128,default='unknown')
	track_num = models.PositiveSmallIntegerField(default=1)

	def __unicode__(self):
		return self.file_name

	def save(self, *args, **kwargs):
		#self.file_name = splitext(self.file_name)[0]
		if not self.pk: #file is new
			md5 = hashlib.md5()
			for chunk in self.songfile.chunks():
					md5.update(chunk)
			self.md5sum = md5.hexdigest()
		super(Song,self).save(*args, **kwargs)

	def update(self):
		audiofile = ID3(self.songfile.path)

		self.title = audiofile["TIT2"]
		self.artist = audiofile["TPE1"]
		tmp = audiofile["TRCK"]
		tmp = str(tmp).split("/",1)
		self.track_num = tmp[0]
		super(Song,self).save()

class Playlist(models.Model):
	owner = models.CharField(max_length=30,default=None)
	title = models.CharField(max_length=128,default='untitled')
	songs = models.ManyToManyField(Song)

	def __unicode__(self):
		return self.title