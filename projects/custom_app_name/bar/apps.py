#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.apps import AppConfig


class BarConfig(AppConfig):
    name = 'bar'  # app 名称，可以 import 的路径, 比如 foo.bar.foobar
    verbose_name = '2名称2'   # 后台显示的名称
