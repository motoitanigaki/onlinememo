# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from onlinememo2.models import *
from django.contrib import admin


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at')

class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.get_fields()]

admin.site.register(Note, NoteAdmin)
admin.site.register(Tag, TagAdmin)