# -*- coding: utf-8 -*-
from django import forms 
from music_stream.models import Song

class SongForm(forms.ModelForm):
	songfile = forms.FileField(
		label = 'Select a file'	
	)

	class Meta:
		model = Song
		fields=('songfile',)
		exclude=('file_name','title','artist','track_num')

