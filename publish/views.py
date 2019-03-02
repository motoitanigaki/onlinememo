from django.http import Http404
from django.views.generic import ListView, DetailView
from onlinememo2.models import Note


class NoteListView(ListView):
    model = Note
    template_name = "notes/note_list.html"


class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.publishment_status == 'UR':
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            raise Http404("このメモは非公開です。")
