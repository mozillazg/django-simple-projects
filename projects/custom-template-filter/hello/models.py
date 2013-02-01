#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, help_text=u'姓名')

    def __unicode__(self):
        return self.name
