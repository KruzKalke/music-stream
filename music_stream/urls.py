from django.conf.urls import patterns, url
from django.conf import settings
from music_stream import views
from django.conf.urls.static import static

urlpatterns = patterns('',
		url(r'^list/$', views.list , name='list'),
        url(r'^$', views.index, name='index'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


