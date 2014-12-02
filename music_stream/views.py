from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models import Q

from music_stream.models import  Song
from music_stream.models import Result
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
		songList = Song.objects.filter(owner=request.user.username)

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
			if 'purge_all' in request.POST:
				for s in songList:
					blobstore.delete(s.songfile.file.blobstore_info.key())
				songList.delete()
			if 'purge_selection' in request.POST:
				for s in songList:
					if str(s) in request.POST:
						blobstore.delete(s.songfile.file.blobstore_info.key())
						s.delete()

		form = SongForm() # A empty, unbound forms

			# Load documents for the list page
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
	

	if request.user.is_authenticated():
		if request.method == 'POST':
			if 'search_submit' in request.POST:
				context_dict = {}
				context_dict['artists'] = None
				context_dict['songs'] = None
				context_dict['albums'] = None
				context_dict['query'] = None
				query = request.POST['query'].strip()
				if query:
					query2 = slugify(query)
					artistz = set([s.artist for s in Song.objects.filter(owner=request.user.username)])
					for a in artistz.copy():
						if not(query in a) and not(query in str(slugify(a))):
							artistz.remove(a)
					albumz = set([s.album for s in Song.objects.filter(owner=request.user.username)])
					for a in albumz.copy():
						if not(query in a) and not(query in str(slugify(a))):
							albumz.remove(a)
					songs = set([s for s in Song.objects.filter(owner=request.user.username)])
					for a in songs.copy():
						if not(query in a.title) and not(query in str(slugify(a.title))):
							songs.remove(a)
					albums = []
					artists = []
					for a in albumz:
						b= Result(item=a, item_slug=slugify(a))
						albums.append(b)
					for a in artistz:
						b= Result(item=a, item_slug=slugify(a))
						artists.append(b)

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
			return HttpResponseRedirect(reverse('music_stream.views.index'))

	else:
		return redirect('accounts/login', request)


def album(request,album_name_slug):
	context_dict = {}
	songs = Song.objects.filter(owner=request.user.username).filter(album_slug=album_name_slug)
	context_dict['songs'] = songs
	context_dict['self'] = album_name_slug

	if request.method == 'POST':
		if 'purge_all' in request.POST:
			for s in songs:
				blobstore.delete(s.songfile.file.blobstore_info.key())
			songs.delete()
		if 'purge_selection' in request.POST:
			for s in songs:
				if str(s) in request.POST:
					blobstore.delete(s.songfile.file.blobstore_info.key())
					s.delete()


	return render(request, 'music_stream/album.html',context_dict)

def artist(request,artist_name_slug):
	context_dict = {}
	albums = Song.objects.filter(owner=request.user.username).filter(artist_slug=artist_name_slug).order_by().values('album','album_slug')
	songs = Song.objects.filter(owner=request.user.username).filter(artist_slug=artist_name_slug)
	
	context_dict['songs'] = songs
	context_dict['self'] = artist_name_slug
	context_dict['albums'] = albums
	if request.method == 'POST':
		if 'purge_all' in request.POST:
			for s in songs:
				blobstore.delete(s.songfile.file.blobstore_info.key())
			songs.delete()
		if 'purge_selection' in request.POST:
			for s in songs:
				if str(s) in request.POST:
					blobstore.delete(s.songfile.file.blobstore_info.key())
					s.delete()

	return render(request, 'music_stream/artist.html',context_dict)

def serve(request, pk):
	upFile = get_object_or_404(Song, pk=pk)
	return serve_file(request, upFile.songfile, save_as=True)

# Create your views here.

def blob(request):
	if request.user.is_authenticated():
		songList = Song.objects.all()
		error= ''
		if request.method == 'POST':
			if request.user.username == 'test':
				if 'purge_all' in request.POST:
					for s in songList:
						blobstore.delete(s.songfile.file.blobstore_info.key())
					songList.delete()
				if 'purge_selection' in request.POST:
					for s in songList:
						if str(s) in request.POST:
							blobstore.delete(s.songfile.file.blobstore_info.key())
							s.delete()
			else:
				error= 'You\'re not authorized to do that...'
		
		return render_to_response(
								'music_stream/list.html',
								{'songList': songList, 'error': error},
								context_instance=RequestContext(request)
								)
	else:
		return redirect('accounts/login', request)