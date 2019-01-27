# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, unique=True, max_length=128)
    title = models.CharField(blank=True, max_length=1024)
    content = models.TextField(blank=True, max_length=524288)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_markdown = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class Tag(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    name = models.CharField(primary_key=True, unique=True, max_length=128)

    def __str__(self):
        return str(self.name)
