from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Teacher
# Create your views here.


class TeacherListView(ListView):
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 50


class TeacherDetailView(DetailView):
    model = Teacher
    slug_field = "username"
    slug_url_kwarg = "username"


def teacher_profile_page(request, username):
    teacher = get_object_or_404(Teacher, username=username)
    context = {
        'teacher': teacher,
    }
    return render(request, 'teachers/teacher-profile.html', context)
