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
			newmusic= Music(name=request.POST["name"], musicfile= request.FILES['musicfile'])
			newmusic.save()
		# Redirect to the document list after POST
			#return HttpResponse("SUCCESS")
			return HttpResponseRedirect(reverse('music_stream.views.list'))
	else:
		form = MusicForm() # A empty, unbound forms

		# Load documents for the list page
	musics = Music.objects.all()
		# Render list page with the documents and the form
	return render_to_response(
						'music_stream/list.html',
						{'musics': musics, 'form': form},
						context_instance=RequestContext(request)
						)

# Create your views here.
