from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from music_stream.models import  Music 
from music_stream.forms import MusicForm


def index(request):
	return render(request, 'music_stream/index.html')

def list(request):
     # Handle file upload
	if request.method == 'POST':
		form = MusicForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			# Redirect to the document list after POST
			return HttpResponse("SUCCESS")
	else:
		form = MusicForm() # A empty, unbound form
		return render_to_response(
						'music_stream/list.html',
						{'form': form}
						)
# Create your views here.
