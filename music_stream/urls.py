from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib import admin
from music_stream import views
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


