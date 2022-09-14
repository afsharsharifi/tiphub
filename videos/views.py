from .models import Video
from django.views.generic import ListView, DetailView

# Create your views here.


class VideoListView(ListView):
    model = Video
    context_object_name = "videos"
    paginate_by = 12


class VideoDetailView(DetailView):
    model = Video
