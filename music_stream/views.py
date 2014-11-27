from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from music_stream.models import  Song
from music_stream.forms import SongForm


def index(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = SongForm(request.POST, request.FILES)
			if form.is_valid():
				newsong= Song(file_name=request.FILES['songfile'].name, songfile= request.FILES['songfile'])
				newsong.save()
				newsong.update()
			# Redirect to the document list after POST
				#return HttpResponse("SUCCESS")
				return HttpResponseRedirect(reverse('music_stream.views.index'))
		else:
			form = SongForm() # A empty, unbound forms

			# Load documents for the list page
		songList = Song.objects.all()
			# Render list page with the documents and the form
		return render_to_response(
							'music_stream/index.html',
							{'songList': songList, 'form': form},
							context_instance=RequestContext(request)
							)
	else:
		# return render(request, 'registration/login.html')
		return redirect('accounts/login', request)



# Create your views here.
