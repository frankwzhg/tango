from django.shortcuts import render, render_to_response
from tango.settings import *
from learn.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json
from django.core import serializers
# Create your views here.
from os import walk
def video(request):
    videos = {}
    videos_file = VideosModel.objects.all()
    videos_file = serializers.serialize('json', videos_file)
    # path = MEDIA_URL + "learn/"
    # path = BASE_DIR + path
    # files = []
    # for (dirpath, dirname, filename) in walk(path):
    #     files.extend(filename)
    # videos["playlist1"] = files
    # videos['media'] = MEDIA_URL
    video_json = json.dumps(videos_file)
    return HttpResponse(video_json)

    # return render(request, "learn/player.html", videos)
    # return render_to_response('learn/player.html', videos)

def video_upload_view(request):
    user = request.user
    if request.method == 'POST':
        print request.POST.get('video_name')
        form = Video_Upload_Form(request.POST)
        print form
        if form.is_valid():
            form_count = form.save(commit=False)
            form_count.video_owner = user
            form_count.user_id = request.user.id
            if 'video_path' in request.FILES:
                form_count.video_path = request.FILES['video_path']
                print form_count.video_path
            form_count.save()
            return HttpResponse('your upload sccuess')

    return render_to_response('learn/video_upload.html', {}, RequestContext(request))