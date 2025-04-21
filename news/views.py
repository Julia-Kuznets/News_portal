from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

class PostsList(ListView):
    model = Post
    ordering = 'date_created'
    template_name = 'posts.html' #шаблон для отображения
    context_object_name = 'posts' #имя переменной в шаблоне

    #пример работы метода для передачи дополнительного контекста (создания переменных, отсутствующих в модели)
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #
    #     return context

class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'


