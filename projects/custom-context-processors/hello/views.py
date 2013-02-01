#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader


# 第一种用法
def index(request):
    return render_to_response('index.html', {'foo': 'bar'},
                              context_instance=RequestContext(request))

# 第二种用法
def hello(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, {'foo': 'bar'})
    return HttpResponse(t.render(c))
