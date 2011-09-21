from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required

from encoder import models as encoder 

def demo_video(request, identifier):
    v = encoder.Video.objects.get(identifier=identifier)
    return render_to_response('encoder/demo/video.html', {'video' : v})

def demo_audio(request, identifier):
    a = encoder.Audio.objects.get(identifier=identifier)
    return render_to_response('encoder/demo/audio.html', {'audio' : a})

@login_required
def encode_collection(request, collection_slug):
    encoder.Collection.objects.get(slug=collection_slug).encode()
    return redirect('/admin/encoder/collection')

@login_required
def import_collection(request, collection_slug):
    c = encoder.Collection.objects.get(slug=collection_slug)
    c.import_media()
    return redirect('/admin/encoder/collection/' + str(c.id) )