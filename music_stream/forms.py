from django import forms 

class UploadSongForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
