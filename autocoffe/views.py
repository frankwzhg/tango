from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
# Create your views here.
import serial
import struct
ser = serial.Serial('/dev/ttyUSB1', 9600)
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
        ser.write(struct.pack('>2B', 2, 0))
    return render_to_response('autocoffee/index.html', {}, RequestContext(request))