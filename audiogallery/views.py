# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import MyAudioFile
import json
import sys
from django.core import serializers
from math import sqrt
from audiofield.forms import *
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    print request
    print request.POST
    i = None
    if request.FILES:
        i = MyAudioFile(audio_file=request.FILES['audio_file'])
        #i.save()
    curr_iv = calculate_ivector(i)
    i.ivector = json.dumps(curr_iv)
    i.save()
    return HttpResponse("Here's the text of the Web page.")


@csrf_exempt
def getaudiofromid(request, id):
    print 'inside getaudiofromid'
    audio_id = MyAudioFile.get(id=id)
    object_name = audio_id.audio_file
    filename = object_name.file.name.split("/")[-1]
    response = HttpResponse(object_name.file, content_type='audio')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


@csrf_exempt
def uploadFile_Query(request):
    if request.FILES:
        i = MyAudioFile(audio_file=request.FILES['audio_file'])
        curr_iv = calculate_ivector(i)
        i.ivector = json.dumps(curr_iv)

    allaudios = MyAudioFile.objects.all()  ##TODO: NOT a Good thing to do
    min_dist = sys.maxint
    min_ind = sys.maxint
    print 'All Audios: ', len(allaudios)
    for audio_i in range(len(allaudios)):
        audio_iv = jsonDec.decode(allaudios[audio_i].ivector)
        dist_i = dist(audio_iv, curr_iv)
        if dist_i < min_dist:
            min_dist = dist_i
            min_ind = audio_i

    res_audio_id = allaudios[min_ind].id
    #i.save()

    return HttpResponse(res_audio_id)

#@csrf_exempt
def upload(request):
    response = render(request, 'upload.html')
    return response

def audio(request):
    response = render(request, 'audio.html')
    return response

def common_audiofield(request):
    response = render(request, 'common_audiofield.html')
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


    # form = CustomerAudioFileForm()
    # form.audio_file = allaudios[0].audio_file
    # form.fields['audio_file'].widget = CustomerAudioFileWidget()
    # data = {'audio_form': form,}
    # data_only_file = {'audio_file':  allaudios[0].audio_file }
    # print data_only_file
    # # return render_to_response(template, data, context_instance=RequestContext(request))
    # # return render_to_response(
    # #     'common_audiofield.html',
    # #     {'allaudios': allaudios, 'form': form}
    # # )
    # data = json.dumps(list(data_only_file), cls=DjangoJSONEncoder)