from django.urls import path
from . import views

urlpatterns = [
    path('<username>', views.teacher_profile_page, name="teacher_profile"),
]
