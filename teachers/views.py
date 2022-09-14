from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Teacher
# Create your views here.


class TeacherListView(ListView):
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 16


class TeacherDetailView(DetailView):
    model = Teacher
    slug_field = "username"
    slug_url_kwarg = "username"
