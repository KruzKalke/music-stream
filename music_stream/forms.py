from django import forms 

class MusicForm(forms.Form):
	title = forms.CharField(max_length=50)
	musicfile = forms.FileField(
		label = 'Select a music file',
		help_text = 'max, 42 mb'
	)
