from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class VideosModel(models.Model):

    video_name = models.CharField(max_length=128, unique=True)
    video_path = models.ImageField(upload_to='learn')
    upload_date = models.DateField(default=datetime.date.today())
    video_owner = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.video_name
