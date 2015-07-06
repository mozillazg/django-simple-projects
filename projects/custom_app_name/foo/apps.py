#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.apps import AppConfig


class FooConfig(AppConfig):
    name = 'foo'  # app 名称，可以 import 的路径, 比如 foo.bar.foobar
    verbose_name = '1名称1'   # 后台显示的名称
