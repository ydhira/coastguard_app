# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import MyAudioFile
import json
import sys
from math import sqrt
from django.core import serializers
import mimetypes

ivector_dim = 64
jsonDec = json.decoder.JSONDecoder()
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
    i = None
    if request.FILES:
        i = MyAudioFile(audio_file=request.FILES['audio_file'])
        #i.save()
    curr_iv = calculate_ivector(i)
    i.ivector = json.dumps(curr_iv)
    i.save()
    return HttpResponse("Here's the text of the Web page.")


@csrf_exempt
def getsimilaraudio(request):
    if request.FILES:
        curr_file = request.FILES['audio_file']
        i = MyAudioFile(audio_file=request.FILES['audio_file'])
        curr_iv = calculate_ivector(i)
        i.ivector = json.dumps(curr_iv)

    allaudios = MyAudioFile.objects.all()

    min_dist = sys.maxint
    min_ind = sys.maxint
    print 'All Audios: ', len(allaudios)
    #print mimetypes.guess_type(allaudios[0])
    for audio_i in range(len(allaudios)):
        audio_iv = jsonDec.decode(allaudios[audio_i].ivector)
        dist_i = dist(audio_iv, curr_iv)
        if dist_i < min_dist:
            min_dist = dist_i
            min_ind = audio_i

    res_audio = allaudios[min_ind]
    #i.save()
    print type(res_audio.audio_file)
    #print res_audio.audio_file.read()
    #print type(res_audio.audio_file.read())
    res_audio = allaudios[len(allaudios)-1]
    print res_audio.audio_file
    data = {}
    data['similar_audio'] = res_audio.audio_file.read()
    response = render(request,'audio.html', data)
    HttpResponseRedirect('audio.html')
    return response

    ####################
    # data = serializers.serialize('json', [res_audio])
    # return HttpResponse(data, content_type='audio')

#@csrf_exempt
def upload(request):
    response = render(request, 'upload.html')
    return response

def audio(request):
    response = render(request, 'audio.html')
    return response

######################################### HELPER FUNCTION #######################################

### Fix this to a real ivector return
def calculate_ivector(curr_audio_file):
    iv = []
    for i in range(ivector_dim):
        iv.append(0)
    return iv

def dist(audio_iv, curr_iv):
    dist = 0
    for (xa, xb) in zip(audio_iv, curr_iv):
        dist += (xa-xb) ^ 2
    return sqrt(dist)
    #np.linalg.norm(audio_iv - curr_iv)

