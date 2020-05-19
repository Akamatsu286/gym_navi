from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse

from .models import Post

class postindex(ListView):
    context_object_name = 'posts'
    template_name = 'post/index.html'
    model = Post
    paginate_by = 10

class postdetail(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post_detail'

class postcreate(CreateView):
    model = Post
    template_name = 'post/form.html'
    fields = ['title','text']
    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})

class postupdate(UpdateView):
    model = Post
    template_name = 'post/form.html'
    fields = ['title','text']
    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})
    