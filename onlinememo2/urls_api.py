# coding: utf-8

from rest_framework import routers
from .views import NoteViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)