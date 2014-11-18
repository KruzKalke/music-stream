# -*- coding: utf-8 -*-
from django import forms 
from music_stream.models import Music

class MusicForm(forms.ModelForm):
	name = forms.CharField(max_length=128, required=True,help_text="name:")
	musicfile = forms.FileField(
		label = 'Select a file'	
	)

	class Meta:
		model = Music
		fields=('name','musicfile',)

