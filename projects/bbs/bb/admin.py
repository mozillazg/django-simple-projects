#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from bb.models import UserProfile
from bb.models import Node
from bb.models import Topic
from bb.models import Reply


# 将 UserProfile 附加到后台的 Users 项中
class UserProfileInline(admin.StackedInline):
    """docstring
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    """docstring
    """
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class NodeAdmin(admin.ModelAdmin):
    """docstring
    """
    pass


class TopicAdmin(admin.ModelAdmin):
    """docstring
    """
    pass


class ReplyAdmin(admin.ModelAdmin):
    """docstring
    """
    pass

admin.site.register(Node, NodeAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)
