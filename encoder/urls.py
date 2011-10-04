from django.conf.urls.defaults import patterns, include, url

from djnco.encoder import views as enc_views

urlpatterns = patterns('',
    url(r'encode_collection/(?P<collection_slug>\w+)',
        enc_views.encode_collection,
        name='encode_collection'),
    url(r'import_collection/(?P<collection_slug>\w+)', 
        enc_views.import_collection, 
        name='import_collection'),
    url(r'list/',
        enc_views.list_media,
        name='list_media'),
    url(r'video/(?P<identifier>[\w\d\-]+)', 
        enc_views.demo_video,
        name='demo_video'),
    url(r'audio/(?P<identifier>[\w\d\-]+)', 
        enc_views.demo_audio,
        name='demo_audio'),
)
