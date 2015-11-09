from learn.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
# Create your views here.


def video(request):
    videos_file = VideosModel.objects.all()
    videos_file = serializers.serialize('json', videos_file)
    return HttpResponse(videos_file, content_type='application/json')

def video_upload_view(request):
    arg = {}
    user = request.user
    if request.method == 'POST':
        form = Video_Upload_Form(request.POST)
        if form.is_valid():
            form_count = form.save(commit=False)
            form_count.video_owner = user
            form_count.user_id = request.user.id
            if 'video_path' in request.FILES:
                form_count.video_path = request.FILES['video_path']
                print form_count.video_path
            form_count.save()
            arg['sccuess'] = "your file uploaded sccuessfully!"
            return HttpResponseRedirect('/learn/')

    # return render_to_response('learn/player.html', arg, RequestContext(request))