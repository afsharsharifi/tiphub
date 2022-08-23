from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Teacher
# Create your views here.


def teacher_profile_page(request, username):
    teacher = get_object_or_404(Teacher, username=username)
    context = {
        'teacher': teacher,
    }
    return render(request, 'accounts/teacher-profile.html', context)
