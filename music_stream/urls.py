from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib import admin
from music_stream import views
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
		url(r'^serve/(?P<pk>.+)$', views.serve, name='serve'),
		url(r'^purge/$', views.purge , name='purge'),
		url(r'^purgeall/$', views.purgeall , name='purgeall'),
        url(r'^$', views.index, name='index'),
        url(r'^search$', views.search, name='search'),
        url(r'^album/(?P<album_name_slug>[\w\-]+)/$', views.album, name='album'),
        url(r'^artist/(?P<artist_name_slug>[\w\-]+)/$', views.artist, name='artist'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


