from django import forms
from autocoffe.models import *

class IP_Add_Form(forms.ModelForm):
    class Meta:
        model = IPaddressModel
        fields = ('name', 'ip_address',)