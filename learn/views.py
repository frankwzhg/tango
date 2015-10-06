from django.shortcuts import render
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

    return render(request, "learn/player.html", videos)