from django.urls import path
from . import views


app_name = "teachers"


urlpatterns = [
    path('<username>', views.teacher_profile_page, name="teacher_profile"),
]
