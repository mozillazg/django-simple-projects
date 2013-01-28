import math

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from djang.contrib.auth import authentricate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from bb.models import Node
from bb.models import Topic
from bb.models import Reply


def index(request):
    page_num = request.GET.get('p', 1)
    nodes = Node.objects.all()
    count = nodes.count()
    limit = 3
    offset = limit * int(page_num) + 1
    nodes = nodes[offset: offset + limit]
    page_count = [i for i in range(1, int(math.ceil(count / float(limit))) +
                  1)]

    context = {
        'nodes': nodes,
        'page_count': page_count,
        'user': request.user,
    }
    return render_to_response('index.html', context)


def node(request, node_id):
    page_num = request.GET.get('p', 1)
    node = Node.objects.get(id=node_id)
    topics = Topic.objects.filter(node=node).order_by('-id')
    count = topic.count()
    limit = 5
    offset = limit * int(page_num) + 1
    topics = topics[offset: offset + limit]
    page_count = [i for i in range(1, int(math.ceil(count / float(limit))) +
                  1)]

    context = {
        'topics': topics,
        'page_count': page_count,
        'user': request.user,
    }
    return render_to_response('node.html', context)


class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


def topic(request, topic_id):
    page_num = request.GET.get('p', 1)
    topic = Topic.objects.get(id=topic_id)
    replies = Reply.objects.filter(topic=topic).order_by('-id')
    count = replies.count()
    limit = 3
    offset = limit * int(page_num) + 1
    replies = replies[offset: offset + limit]
    page_count = [i for i in range(1, int(math.ceil(count / float(limit))) +
                  1)]
    form = ReplyForm()

    context = {
        'topic': topic,
        'page_count': page_count,
        'user': request.user,
        'replies': replies,
        'form': form,
    }
    return render_to_response('topic.html', context)


def reply(request, topic_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            form = ReplyForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                username = user.username
                user = User.objects.get(username=username)
                topic = Topic.objects.get(id=topic_id)
                reply_ = Reply(user=user, topic=topic, content=content)
                reply_.save()
                return HttpResponseRedirect('/topic/%s/' % str(topic.id))
    return HttpResponseRedirect('/accounts/login/')


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ['user']


def create_topic(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            node_title = form.cleaned_data['node']
            username = user.username
            user = User.objects.get(username=username)
            node = Node.objects.get(title=node_title)
            topic = Topic(title=title, node=node, content=content, user=user)
            topic.save()
            return HttpResponseRedirect('/topic/%s/' % str(topic.id))
    else:
        form = CreateTopicForm()
    return render_to_response('create.html', {'form': form, 'user': user})


class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = SignUpForm()
    return render_to_response('signup.html', {'form': form})


class LogInForm(SignUpForm):
    def __init__(self, *args, **kwargs):
        SignUpForm.__init__(self, *args, **kwargs)
        if 'email' in self.fields:
            del self.fields['email']


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authentricate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LogInForm()
    return render_to_response('signup.html', {'form': form})


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


def account(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = user.username
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = LogInForm()
    return render_to_response('account.html', {'form': form, 'user': user})
