from accounts.models import UserIP
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, View

from .models import Comment, Like, Video


class VideoListView(ListView):
    model = Video
    paginate_by = 12


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, slug=self.kwargs['slug'])
        user_ip, is_created = UserIP.objects.get_or_create(user_ip=request.META.get('REMOTE_ADDR'))
        video.viewers_by_ip.add(user_ip)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        video = get_object_or_404(Video, slug=self.kwargs['slug'])
        comment = self.request.POST.get('comment_body')
        parent_id = int(self.request.POST.get('parent_id'))
        if parent_id != 0:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            Comment.objects.create(user=user, video=video, parent=parent_comment, comment=comment)
        else:
            Comment.objects.create(user=user, video=video, parent=None, comment=comment)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = get_object_or_404(Video, slug=self.kwargs['slug'])
        _list = Comment.objects.filter(video=video, parent=None)
        paginator = Paginator(_list, 5)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        if self.request.user.is_authenticated:
            context["is_liked"] = self.request.user.likes.filter(video=self.object.id).exists()
        else:
            context["is_liked"] = False
        context["likes_count"] = video.likes.filter(video=self.object.id).count()
        context["views"] = Video.objects.annotate(num_views_ip=Count('viewers_by_ip'),).order_by('-viewers_by_ip')
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
