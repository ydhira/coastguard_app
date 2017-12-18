# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import MyAudioFile


# Create your views here.

def index(request):
    print 'rendering index.html'
    response = render(request, 'index.html')
    return response


@csrf_exempt
def fileupload(request):
    print 'inside views - file upload '
    print type(request.FILES), request.FILES
    print type(request.FILES['audio_file']), request.FILES['audio_file']
    print request.FILES['audio_file'].size
    if request.FILES:
        i = MyAudioFile(audio_file=request.FILES['audio_file'])
        print vars(MyAudioFile.audio_file.field)
        i.save()

    
    return HttpResponse("Here's the text of the Web page.")


#@csrf_exempt
def upload(request):
    response = render(request, 'upload.html')
    return response
