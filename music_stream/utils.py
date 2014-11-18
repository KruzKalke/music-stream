from music_stream import models

def handle_upload_file(f):
	with open('/media/filename', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
