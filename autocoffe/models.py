from django.db import models

# Create your models here.
class IPaddressModel(models.Model):
    name = models.CharField(max_length=128)
    ip_address = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name