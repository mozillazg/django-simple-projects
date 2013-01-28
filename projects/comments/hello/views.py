from django.shortcuts import render_to_response
from django.template import RequestContext
from hello.models import Topic


def index(request):
    # return render_to_response('index.html', {}, RequestContext(request))
    topics = Topic.objects.all()
    return render_to_response('index.html', {'topics': topics})


def display_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render_to_response('topic.html', {'topic': topic},
                              RequestContext(request))
