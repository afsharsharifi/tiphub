from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Teacher
from videos.models import Video
from accounts.models import CustomUser


class TeacherListView(ListView):
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 16


class TeacherDetailView(DetailView):
    model = Teacher
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, username=self.kwargs["username"])
        views = Video.objects.filter(teacher=teacher).aggregate(Sum("viewers_by_ip"))
        context["video_views"] = views["viewers_by_ip__sum"]
        return context
