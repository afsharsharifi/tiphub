from .models import Like, Video
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.


class VideoListView(ListView):
    model = Video
    context_object_name = "videos"
    paginate_by = 12


class VideoDetailView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_liked"] = self.request.user.likes.filter(video=self.object.id).exists()
        context["likes_count"] = self.request.user.likes.filter(video=self.object.id).count()
        return context


class LikeVideoView(View):
    def get(self, request, id):
        video = get_object_or_404(Video, id=id)
        like = Like.objects.filter(user=request.user, video=video)
        if like.exists():
            like.delete()
            return JsonResponse({"response": "dislike", "count": video.likes.count()})
        Like.objects.create(user=request.user, video=video)
        return JsonResponse({"response": "like", "count": video.likes.count()})
