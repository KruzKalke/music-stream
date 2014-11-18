from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



def index(request):
	if request.user.is_authenticated():
		return render(request, 'music_stream/index.html')
	else:
		return render(request, 'registration/login.html')
# Create your views here.
