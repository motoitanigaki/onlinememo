# coding: utf-8

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *


class TagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(TagSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Tag
        fields = ('note', 'user', 'name')

class NoteSerializer(serializers.ModelSerializer):

    tags = SerializerMethodField()

    class Meta:
        model = Note
        fields = ('id', 'user', 'title', 'content', 'created_at', 'updated_at', 'tags')

    def get_tags(self, obj):
        try:
            tags = TagSerializer(Tag.objects.all().filter(note = Note.objects.get(id=obj.id)), many=True).data
            tag_abstruct_contents = []
            for tag in tags:
                tag_abstruct_contents.append(tag['name'])
            return tag_abstruct_contents
        except:
            tag_abstruct_contents = None
            return tag_abstruct_contents