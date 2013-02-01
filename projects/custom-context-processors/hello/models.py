#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
