import subprocess
import os
import shutil
import datetime

from django.conf import settings

from celery.task import task


@task(name="encode-video")
def encode_video(video):
    video.encode_start_time = datetime.datetime.now()
    video.save()
    ffmpeg = '/usr/local/bin/ffmpeg'
    for bitrate in settings.VIDEO_BITRATES:
        command = [ffmpeg,
                    #'-g', '250',
                    #'-r', '20',
                    '-i', video.encode_src(),
                    '-acodec', 'libfaac',
                    '-async', '1',
                    '-ar', '44100',
                    '-ab', '96k',
                    '-vcodec', 'libx264',
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                    #'-vpre', 'medium',
                    '-b', str(bitrate) + 'k',
                    '-threads', '6',
                    '-vf', 'scale=iw:trunc(ih/2)*2',
                    '-y',
                    video.encode_dst(bitrate)]
        proc = subprocess.Popen(command)
        proc.wait()
        shutil.move(video.encode_dst(bitrate), video.publish_path(bitrate))
    video.encode_end_time = datetime.datetime.now()
    video.encoding_finished = True
    video.save()
    os.remove(video.encode_src())


@task(name="encode-audio")
def encode_audio(audio, bitrate=128):
    audio.encode_start_time = datetime.datetime.now()
    audio.save()
    ffmpeg = '/usr/bin/ffmpeg'
    command = [ffmpeg,
                '-i', audio.encode_src(),
                '-acodec', 'libmp3lame',
                '-ab', str(bitrate) + 'k',
                '-threads', '6',
                '-y',
                audio.encode_dst(bitrate)]
    proc = subprocess.Popen(command)
    proc.wait()
    shutil.move(audio.encode_dst(bitrate), audio.publish_path(bitrate))
    audio.encode_end_time = datetime.datetime.now()
    audio.encoding_finished = True
    audio.save()
    os.remove(audio.encode_src())
