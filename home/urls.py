from django.urls import path

from . import views

app_name = "home"


urlpatterns = [
    path('', views.HomePageView.as_view(), name="index"),
    path("search/", views.VideoSerachView.as_view(), name="search_video"),
]
