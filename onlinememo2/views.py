import django_filters
import datetime
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.response import Response
from .serializer import NoteSerializer, TagSerializer
from .models import Note, Tag

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            notes = Note.objects.filter(user=self.request.user)
            for note in notes:
                note.created_at = note.created_at.strftime('%Y/%m/%d %H:%M')
                note.updated_at = note.updated_at.strftime('%Y/%m/%d %H:%M')
            return notes
        else:
            # TODO loginしていない際のエラーレスポンス送信方法調査
            # return Response({'errors': ['You need to login']}, status=status.HTTP_400_BAD_REQUEST)
            None

    # create関数内で使うget_serializerをオーバーライド
    # https://stackoverflow.com/questions/43525860/django-rest-framework-cannot-deal-with-multple-objects-in-model-viewset/43526936
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(NoteViewSet, self).get_serializer(*args, **kwargs)

    # post
    def create(self, request):

        for posted_note in request.data:
            posted_note['created_at'] = datetime.datetime.strptime(posted_note['created_at'], '%Y/%m/%d %H:%M')
            posted_note['updated_at'] = datetime.datetime.strptime(posted_note['updated_at'], '%Y/%m/%d %H:%M')

            note, created = Note.objects.update_or_create(
                id=posted_note['id'],
                user=request._user,
                defaults={
                    'title': posted_note['title'],
                    'content': posted_note['content'],
                    'publishment_status': posted_note['publishment_status'],
                    'created_at': posted_note['created_at'],
                    'updated_at': posted_note['updated_at']
                }
            )

            for tag in Tag.objects.filter(user=request._user,note=note):
                tag.delete()
            for posted_tag in posted_note['tags']:
                Tag.objects.create(user=request._user,note=note,name=posted_tag)

        # TODO post時にlocal storage内の全ノートを送り、update_or_createするが、下記createメソッドデフォルトの
        # 挙動とロジック的にバッティングするので400ステータスが返ってしまう 要調査
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer