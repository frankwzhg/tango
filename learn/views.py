from django.shortcuts import render, render_to_response
from tango.settings import *

# Create your views here.
from os import walk
def video(request):
    videos = {}
    path = MEDIA_URL + "learn/"
    path = BASE_DIR + path
    files = []
    for (dirpath, dirname, filename) in walk(path):
        files.extend(filename)
    videos["playlist1"] = files
    videos['media'] = MEDIA_URL
    print videos

    # return render(request, "learn/player.html", videos)
    return render_to_response('learn/player.html', videos)