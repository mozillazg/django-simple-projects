#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hello.models import Category


def categories(request):  # 只有一个参数（HttpRequeset 对象）
    all_categories = Category.objects.all()
    context = {'categories': all_categories}

    return context  # 返回值必须是个字典
