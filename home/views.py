from django.shortcuts import render
from django.views.generic import TemplateView
from videos.models import Video
# Create your views here.


class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_videos'] = Video.objects.all().order_by('-published_at')[:5]
        context['top_videos'] = Video.objects.all().order_by('-viewers_by_ip')[:5]
        return context
