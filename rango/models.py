from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    Category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)


    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required, links Userprofile to user model instance.
    user = models.OneToOneField(User)

    #The additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # picture = models.ImageField(upload_to='profile_images', blank=True)
    birthday = models.DateField(blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())


    # Override the __unicode__() method to return out something meanningful
    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profile'



# class EModel(models.Model):
#     date = models.DateField(blank=False)