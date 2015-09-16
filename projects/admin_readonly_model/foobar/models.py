from django.db import models


class Foo(models.Model):
    foo = models.CharField(max_length=10)


class Bar(models.Model):
    bar = models.CharField(max_length=10)
