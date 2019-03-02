from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from .views import NoteListView, NoteDetailView

urlpatterns = [
    # path("", NoteListView.as_view(), name='note_list'),
    path("<slug:pk>/", NoteDetailView.as_view(), name='note_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
