from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# from django.http import HttpResponse


def home(request):
    context = {"posting": post.objects.all()}
    return render(request, "wireium/home.html", context)
    # return HttpResponse('<h1> <center>Home</center></h1>')


# Created post views here.
class PostListView(ListView):
    model = post
    template_name = "wireium/home.html"  # <app> /<model>_<viewtype>.html
    context_object_name = "posting"
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = post
    template_name = "wireium/user_post.html"  # <app> /<model>_<viewtype>.html
    context_object_name = "posting"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return post.objects.filter(author=user).order_by("-date_posted")

# Created post detail view
class PostDetailView(DetailView):
    model = post


# Created post create view
class PostCreateView(LoginRequiredMixin ,CreateView):
    model = post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Created post update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "wireium/about.html", {"title": "About"})
    # return HttpResponse('<h1> <center>About</center></h1>')
