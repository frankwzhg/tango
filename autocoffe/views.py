from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from autocoffe.models import *
from django.core import serializers
from django.http import HttpResponse
from autocoffe.forms import *

# Create your views here.
import serial
import struct
ser = serial.Serial('/dev/ttyACM1', 9600)
def relaxtime(request):
    # print request.POST.get('tea')
    if "tea" in request.POST:
        print "test"
        ser.write(struct.pack('>2B', 0, 100))
    elif "cof" in request.POST:
        ser.write(struct.pack('>2B', 0, 50))
    elif 'lightO' in request.POST:
        print "test1"
        ser.write(struct.pack('>2B', 1, 0))
    elif 'lightC' in request.POST:
        print "test2"
        ser.write(struct.pack('>2B', 2, 0))
    return render_to_response('autocoffee/index.html', {}, RequestContext(request))


def auth_ipaddress(request):
    auth_ipaddress_list = IPaddressModel.objects.all()
    auth_opaddress_json = serializers.serialize('json', auth_ipaddress_list)
    return HttpResponse(auth_opaddress_json, content_type='application/json')

def add_ipaddress(request):
    if request.method == "POST":
        form = IP_Add_Form(request.POST)
        print form
        if form.is_valid():
            print "test"
            form_content = form.save(commit=False)
            form_content.name = request.POST.get('name')
            print request.POST.get('name')
            form_content.ip_address = request.POST.get('ip')
            form_content.save()
    return render_to_response('autocoffee/ip_address.html', {}, RequestContext(request))
