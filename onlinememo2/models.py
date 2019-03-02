# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):

    PRIVATE = 'PV'
    PUBLIC = 'PL'
    URL = 'UR'
    PUBLISHMENT_STATUS_CHOICES = (
        (PRIVATE, 'Private'),   # 表示不可。本人が編集閲覧のみ
        (PUBLIC, 'Public'),     # 誰でも閲覧可能
        (URL, 'URL'),           # URLを知っていれば閲覧可能
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, unique=True, max_length=128)
    title = models.CharField(blank=True, max_length=1024)
    content = models.TextField(blank=True, max_length=524288)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_markdown = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    publishment_status = models.CharField(max_length=2, choices=PUBLISHMENT_STATUS_CHOICES, default='PV')

    def __str__(self):
        return str(self.title)

class Tag(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    name = models.CharField(primary_key=True, unique=True, max_length=128)

    def __str__(self):
        return str(self.name)
