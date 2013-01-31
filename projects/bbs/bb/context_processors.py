#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
custome context processors
"""

from bb.models import Node
from bb.models import Topic
from bb.models import Reply
from django.contrib.auth.models import User


def forum_info(request):
    """docstring
    """
    forum_info_ = {}
    forum_info_['members'] = User.objects.filter(is_staff=False,
                                                 is_active=True).count()
    forum_info_['nodes'] = Node.objects.count()
    forum_info_['topics'] = Topic.objects.count()
    forum_info_['replies'] = Reply.objects.count()

    return {'forum_info': forum_info_}
