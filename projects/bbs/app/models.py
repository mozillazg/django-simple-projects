from django.db import models
from django.contrib.auth.models import User


class Node(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class Topic(models.Model):
    node = models.ForeignKey(Node)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    topic = models.ForeignKey(Topic)
    user = models.ForeignKey(User)
    content = models.TextField()

    def __unicode__(self):
        return self.topic.title
