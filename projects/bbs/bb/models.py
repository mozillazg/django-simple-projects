#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""models
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    """额外的用户信息
    """
    user = models.OneToOneField(User)  # 必须

    login_count = models.IntegerField(default=0)


# 创建用户的时同时创建相关的 UserProfile
def create_user_profile(sender, instance, created, **kwargs):
    """docstring
    """
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Node(models.Model):
    """节点
    """
    title = models.CharField(max_length=200)
    # slug = None
    # avatar = models.ImageField(upload_to='static/')
    description = models.CharField(max_length=500)
    topic_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Topic(models.Model):
    """主题
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    node = models.ForeignKey(Node)
    hits = models.IntegerField(default=1)
    reply_count = models.IntegerField(default=0)
    last_reply_by = None
    last_reply_time = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        """docstring
        """
        return ('topic_view', (), {'topic_id': self.id})

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    """主题回复
    """
    topic = models.ForeignKey(Topic)
    user = models.ForeignKey(User)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.topic.title
