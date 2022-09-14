from django.urls import path, re_path
from . import views

app_name = "videos"

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list_view"),
    re_path(r'(?P<slug>[-\w]+)/', views.VideoDetailView.as_view(), name="video_detail_view"),
]
