# -*- coding: utf-8 -*-
from django import forms 
from music_stream.models import Music

class MusicForm(forms.ModelForm):
	musicfile = forms.FileField(
		label = 'Select a file'	
	)

	class Meta:
		model = Music
		fields=('musicfile',)
		exclude=('name',)

