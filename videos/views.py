from .models import Like, Video, Comment
from django.views.generic import ListView, DetailView, View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# Create your views here.


class VideoListView(ListView):
    model = Video
    context_object_name = "videos"
    paginate_by = 12


class VideoDetailView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = get_object_or_404(Video, slug=self.kwargs['slug'])
        _list = Comment.objects.filter(video=video, parent=None)
        paginator = Paginator(_list, 15)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        context["is_liked"] = self.request.user.likes.filter(video=self.object.id).exists()
        context["likes_count"] = self.request.user.likes.filter(video=self.object.id).count()
        return context

    def post(self, *args, **kwargs):
        comment = self.request.POST['comment_body']
        return HttpResponse(comment)


class LikeVideoView(View):
    def get(self, request, id):
        video = get_object_or_404(Video, id=id)
        like = Like.objects.filter(user=request.user, video=video)
        if like.exists():
            like.delete()
            return JsonResponse({"response": "dislike", "count": video.likes.count()})
        Like.objects.create(user=request.user, video=video)
        return JsonResponse({"response": "like", "count": video.likes.count()})
