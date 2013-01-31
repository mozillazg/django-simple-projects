#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django import forms
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from bb.models import Node
from bb.models import Topic
from bb.models import Reply
from bb.models import UserProfile


class SignupForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()


class SigninForm(SignupForm):
    def __init__(self, *args, **kwargs):
        SignupForm.__init__(self, *args, **kwargs)
        if 'email' in self.fields:
            del self.fields['email']


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea())


class CreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('user', 'hits', 'reply_count')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(name, email, password)
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render_to_response('signup.html', {'form': form},
                              context_instance=RequestContext(request))


def change_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = request.user.username
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            logout(request)
            return HttpResponseRedirect('/account/signin')
    else:
        form = ChangePasswordForm()
    return render_to_response('account.html', {'form': form},
                              context_instance=RequestContext(request))


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(username=name, password=password)
            if user:
                if user.is_active:
                    userprofile = UserProfile.objects.get(user=user)
                    userprofile.login_count += 1
                    userprofile.save()
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = SigninForm()
    return render_to_response('signin.html', {'form': form},
                              context_instance=RequestContext(request))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


# def index(request):
    # topics = Topic.objects.all()
    # page_count = [i for i in range(len(topics)/5)] else [0]
    # context =

    # return render_to_response('index.html', {'topics': topics})


def page(request, page_id=1, node_id=0, popular=False):
    nav_name = ''
    topics = Topic.objects.order_by('-last_reply_time')
    if popular:
        topics = topics.order_by('-reply_count', '-last_reply_time')
        nav_name = 'Popular'
    elif node_id:
        node = Node.objects.get(id=node_id)
        topics = topics.filter(node=node)
        count = topics.count()
        nav_name = node.title

    # Pagination
    limit = 10
    paginator = Paginator(topics, limit)
    try:
        topics = paginator.page(page_id)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    user = request.user
    context = {
        'topics': topics,
        'user': user,
        'node_id': node_id,
        'nav_name': nav_name,
    }

    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))


def nodes(request):
    nodes = Node.objects.all()
    nav_name = 'Nodes'
    return render_to_response('nodes.html', {'nodes': nodes,
                              'nav_name': nav_name},
                              context_instance=RequestContext(request))


def topic(request, topic_id, page_id=1):
    topic_ = Topic.objects.get(id=topic_id)
    replies = Reply.objects.filter(topic=topic_).order_by('-created')
    topic_.hits += 1
    topic_.save()

    # Pagination
    limit = 5
    paginator = Paginator(replies, limit)
    try:
        replies = paginator.page(page_id)
    except EmptyPage:
        replies = paginator.page(paginator.num_pages)

    context = {
        'user': request.user,
        'topic': topic_,
        # 'replies': replies,
        # 'form': ReplyForm(),
    }

    return render_to_response('topic.html', context,
                              context_instance=RequestContext(request))


def reply(request, topic_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            name = request.user.username
            user = User.objects.get(username=name)
            content = form.cleaned_data['reply']
            topic_ = Topic.objects.get(id=topic_id)
            reply_ = Reply(topic=topic_, user=user, content=content)
            reply_.save()
            topic_.reply_count += 1
            topic_.save()

            return HttpResponseRedirect('/topic/' + str(topic_id))
    return HttpResponseRedirect('/')


def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            name = request.user.username
            user = User.objects.get(username=name)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            node_title = form.cleaned_data['node']
            node = Node.objects.get(title=node_title)
            topic_ = Topic(title=title, content=content, node=node,
                           user=user)
            topic_.save()
            node.topic_count += 1
            node.save()

            return HttpResponseRedirect('/topic/' + str(topic_.id))
    else:
        form = CreateForm()
        context = {
            'form': form,
        }
    return render_to_response('create.html', context,
                              context_instance=RequestContext(request))
