# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
    response = render(request, 'index.html')
    return response

def fileupload():
    print 'hereeee'