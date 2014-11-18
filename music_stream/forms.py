# -*- coding: utf-8 -*-
from django import forms 

class MusicForm(forms.Form):
	musicfile = forms.FileField(
		label = 'Select a file'	
	)
