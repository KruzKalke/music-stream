from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from music_stream.models import  Song
from music_stream.forms import SongForm

import os
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from filetransfers.api import prepare_upload
from filetransfers.api import serve_file


def index(request):
	upload_url = blobstore.create_upload_url('/')
	view_url = reverse('music_stream.views.index')
	if request.user.is_authenticated():
		if request.method == 'POST':
			if 'upload_submit' in request.POST:
				form = SongForm(request.POST, request.FILES)
				if form.is_valid():
					newsong = Song(owner=request.user.username, file_name=request.FILES['songfile'].name, songfile=request.FILES['songfile'])
					newsong.save()
					newsong.update()
				# Redirect to the document list after POST
					#return HttpResponse("SUCCESS")
					return HttpResponseRedirect(view_url)
		else:
			form = SongForm() # A empty, unbound forms

			# Load documents for the list page
		songList = Song.objects.filter(owner=request.user.username)
		upload_url, upload_data = prepare_upload(request, view_url)
			# Render list page with the documents and the form
		return render_to_response(
							'music_stream/index.html',
							{'songList': songList, 'form': form, 'upload_url': upload_url, 'upload_data': upload_data},
							context_instance=RequestContext(request)
							)
	else:
		return redirect('accounts/login', request)

def search(request):
	context_dict = {}
	context_dict['artists'] = None
	context_dict['songs'] = None
	context_dict['albums'] = None
	context_dict['query'] = None

	if request.user.is_authenticated():
		if request.method == 'POST':
			if 'search_submit' in request.POST:
				query = request.POST['query'].strip()
				if query:
					artists = Song.objects.filter(owner=request.user.username).filter(artist__icontains=query).order_by().values('artist','artist_slug').distinct()
					# search for albums matching the query or albums from the artist matching the query
					albums = Song.objects.filter(owner=request.user.username).filter(Q(album__icontains=query) | Q(artist__icontains=query)).order_by().values('album','album_slug').distinct()


					songs = Song.objects.filter(owner=request.user.username).filter(Q(title__icontains=query) | Q(artist__icontains=query) | Q(album__icontains=query))
					context_dict['query'] = query
					context_dict['artists'] = artists
					context_dict['songs'] = songs
					context_dict['albums'] = albums
					return render(request,'music_stream/search.html',context_dict)

				else:
					return HttpResponseRedirect(reverse('music_stream.views.index'))
		else:
			return HttpResponseRedirect(reverse('music_stream.views.index'))

	else:
		return redirect('accounts/login', request)


def album(request,album_name_slug):
	context_dict = {}
	songs = Song.objects.filter(owner=request.user.username).filter(album_slug__icontains=album_name_slug)
	context_dict['songs'] = songs

	return render(request, 'music_stream/album.html',context_dict)

def artist(request,artist_name_slug):
	context_dict = {}
	albums = Song.objects.filter(owner=request.user.username).filter(artist_slug__icontains=artist_name_slug).order_by().values('album','album_slug').distinct()
	songs = Song.objects.filter(owner=request.user.username).filter(artist_slug__icontains=artist_name_slug)
	context_dict['albums'] = albums
	context_dict['songs'] = songs


	return render(request, 'music_stream/artist.html',context_dict)

def serve(request, pk):
	upFile = get_object_or_404(Song, pk=pk)
	return serve_file(request, upFile.songfile, save_as=True)

def purge(request):
	songList = Song.objects.filter(owner=request.user.username)
	for song in songList:
		blobstore.delete(song.songfile.file.blobstore_info.key())
		song.delete()
	return redirect('/')

def purgeall(request):
	songList = Song.objects.all()
	songList.delete()
	for b in blobstore.BlobInfo.all():
		blobstore.delete(b.key())
	return redirect('/')
# Create your views here.
