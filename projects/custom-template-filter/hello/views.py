from django.shortcuts import render_to_response
from hello.models import User


def index(request):
    users = User.objects.all()
    return render_to_response('index.html', {'users': users})
