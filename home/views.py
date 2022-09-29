from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView
from videos.models import Video, Category
from django.db.models import Q


class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_videos'] = Video.objects.all().order_by('-published_at')[:5]
        context['top_videos'] = Video.objects.all().order_by('-viewers_by_ip')[:5]
        context['categories'] = Category.objects.all()
        return context


class VideoSerachView(ListView):
    model = Video
    template_name = "videos/video_list.html"
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        return self.model.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
