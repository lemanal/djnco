import re

from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required

from encoder import models as encoder 

def add_seek_links(media):
  for mins, secs in re.findall("(\d\d?):(\d\d)", media.description):
    time = int(mins)*60 + int(secs)
    media.description = media.description.replace(":".join((mins,secs)), '<a href="#" onClick="$f(\'player_%s\').seek(%s);">%s:%s</a>' % (media.identifier, str(time), mins, secs) )

def demo_video(request, identifier):
    v = encoder.Video.objects.get(identifier=identifier)
    if v.description:
        add_seek_links(v)
    return render_to_response('encoder/demo/video.html', {'video' : v})

def demo_audio(request, identifier):
    a = encoder.Audio.objects.get(identifier=identifier)
    if a.description:
        add_seek_links(a)
    return render_to_response('encoder/demo/audio.html', {'audio' : a})

def list_media(request):
    media = list(encoder.Video.objects.all()) + list(encoder.Audio.objects.all())
    return render_to_response('encoder/list_media.html', {'media' : media})

@login_required
def encode_collection(request, collection_slug):
    encoder.Collection.objects.get(slug=collection_slug).encode()
    return redirect('/admin/encoder/collection')

@login_required
def import_collection(request, collection_slug):
    c = encoder.Collection.objects.get(slug=collection_slug)
    c.import_media()
    return redirect('/admin/encoder/collection/' + str(c.id) )
