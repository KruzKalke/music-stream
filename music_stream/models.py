from django.db import models
from django.db.models import Model
from django.template.defaultfilters import slugify
from djangotoolbox.fields import ListField
from os.path import splitext
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM, TALB
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage as storage
from os.path import splitext
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM

from google.appengine.ext import blobstore
from google.appengine.api import images

import hashlib

# class CustomStorage(FileSystemStorage):
# 	def get_available_name(self, file_name):
# 		return file_name
		
# 	def _save(self, file_name, content):
# 		if self.exists(file_name):
# 			#if the file exists, do not save the new file
# 			return file_name
# 		#if the file does not exist, save the file
# 		return super(CustomStorage, self)._save(file_name, content)		

class Song(models.Model):
	owner = models.CharField(max_length=30,default=None)
	shared = ListField()
	file_name = models.CharField(max_length=128)
	songfile = models.FileField(upload_to='music/%Y/%m/%d')
	md5sum = models.CharField(max_length=36,default=None)
	title = models.CharField(max_length=128,default='untitled')
	artist = models.CharField(max_length=128,default='unknown')
	album = models.CharField(max_length=128,default='unknown')
	track_num = models.PositiveSmallIntegerField(default=1)
	length = models.PositiveSmallIntegerField(default=0)
	artist_slug = models.SlugField(max_length=128,default='unknown')
	album_slug = models.SlugField(max_length=128,default='unknown')
	title_slug = models.SlugField(max_length=128,default='unknown')


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
	def saveTags(self, *args, **kwargs):
		super(Song,self).save(*args, **kwargs)

	def update(self):
		#s= serve_file(self, self.songfile, save_as=True)
		#s= "/serve/"+ str(self.pk)
		s=self.songfile.file.blobstore_info
		self.shared = ['test']
		# s= blobstore.BlobInfo.get(r)
		# s= self.songfile.file.blobstore_info
		# s = images.get_serving_url(r)
		audiofile = ID3(s)
		mp3file = MP3(s)
		if "TIT2" in audiofile:
			self.title = str(audiofile["TIT2"])
		else:
			self.title = self.file_name
		if "TPE1" in audiofile:
			self.artist = str(audiofile["TPE1"])
		else:
			self.artist = 'Unknown'
		if "TALB" in audiofile:
			self.album = str(audiofile["TALB"])
		else:
			self.album = 'Unknown'
		self.artist_slug = slugify(self.artist)
		self.album_slug = slugify(self.album)
		self.title_slug = slugify(self.title)
		tmp = mp3file.info.length
		tmp = str(tmp).split(".",1)
		self.length = tmp[0]
		if "TRCK" in audiofile:
			tmp = audiofile["TRCK"]
		else:
			tmp = 1
		tmp = str(tmp).split("/",1)
		self.track_num = tmp[0]
		
		super(Song,self).save()
	def share(self, user):
		self.shared.append(user)
		super(Song,self).save()
	def deshare(self, user):
		self.shared.remove(user)
		super(Song,self).save()

class Result(models.Model):
	item = models.CharField(max_length=128,default='unknown')
	item_slug= models.SlugField(max_length=128,default='unknown')

class Playlist(models.Model):
	owner = models.CharField(max_length=30,default=None)
	name = models.CharField(max_length=30,default=None)
	name_slug = models.SlugField(max_length=128,default='unknown')
	songs = ListField()


	def __unicode__(self):
		return self.name


	def save(self, *args, **kwargs):
		self.name_slug = slugify(self.name)
		super(Playlist,self).save(*args, **kwargs)

	def add(self, song):

		self.songs.append(song)
		set(self.songs)
		super(Playlist, self).save()

	def remove(self, song):

		self.songs.remove(song)
		set(self.songs)
		super(Playlist, self).save()