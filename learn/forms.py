from django import forms
from django.contrib.auth.models import User
from learn.models import *


class Video_Upload_Form(forms.ModelForm):
    class Meta:
        model = VideosModel
        fields = ('video_name',)

