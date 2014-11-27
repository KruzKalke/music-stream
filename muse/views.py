
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from muse.music_stream.models	import	Music 
from muse.music_stream.forms import MusicForm 

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            newmusic= Music(musicfile= request.FILES['musicfile'])
            newmusic.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('music_stream.views.list'))
    else:
        form = MusicForm() # A empty, unbound form

    # Load documents for the list page
    musics = Music.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'music_stream/list.html',
        {'musics': documents, 'form': form},
        context_instance=RequestContext(request)
    )
