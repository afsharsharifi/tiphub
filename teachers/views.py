from django.views.generic import DetailView, ListView

from .models import Teacher


class TeacherListView(ListView):
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 16


class TeacherDetailView(DetailView):
    model = Teacher
    slug_field = "username"
    slug_url_kwarg = "username"
