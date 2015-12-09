from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from autocoffe.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from autocoffe.forms import *
from django.views.decorators.csrf import csrf_exempt
import time

# Create your views here.
import serial
import struct
ser = serial.Serial('/dev/ttyACM2', 9600)
def relaxtime(request):
    print request.POST.get('tea')
    if "tea" in request.POST:
        print "test"
        ser.write(struct.pack('>2B', 0, 100))
    elif "cof" in request.POST:
        ser.write(struct.pack('>2B', 0, 50))
    elif 'lightO' in request.POST:
        print "test1"
        ser.write(struct.pack('>2B', 3, 0))
    elif 'lightC' in request.POST:
        print "test2"
        ser.write(struct.pack('>2B', 4, 0))
    return render_to_response('autocoffee/index.html', {}, RequestContext(request))


def auth_ipaddress(request):
    auth_ipaddress_list = IPaddressModel.objects.all()
    auth_opaddress_json = serializers.serialize('json', auth_ipaddress_list)
    return HttpResponse(auth_opaddress_json, content_type='application/json')

def add_ipaddress(request):
    # print delitem.objects.filter(id__in=request.POST.getlist(delitem))
    if (request.method == "POST") and ("ip_submit" in request.POST):
        form = IP_Add_Form(request.POST)
        if form.is_valid():
            form.save()
            # form_content = form.save(commit=False)
            # form_content.name = request.POST.get('uname')
            # print request.POST.get('uname')
            # form_content.ip_address = request.POST.get('ipaddress')
            # form_content.save()
            return HttpResponseRedirect("/coffeebreak/ip_add/")
        else:
            return HttpResponse("you are failed")
    else:
        form = IP_Add_Form()
        return render_to_response('autocoffee/ip_address.html', {'form':form}, RequestContext(request))

@csrf_exempt
def delete(request):
    candidate = IPaddressModel.objects.get(ip_address=request.REQUEST['ip_address'])
    candidate.delete()
    return HttpResponseRedirect("/coffeebreak/ip_add/")

# def get_serial_value(request):
#
#     # ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0)
#     data = []
#     time0 = time.time()
#
#     while (time.time() -time0 <= 90):
#         data.append(ser.readline()[0:1])
#         # time.sleep(18)
#     print data
#     return HttpResponse(data)

