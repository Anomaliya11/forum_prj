import csv
import datetime
from urllib import response

from urllib.parse import urlparse
from django.shortcuts import render, redirect
from service.models import Post, Comment
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from .forms import PostForm, CommentForm, UserRegisterForm, MessageForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from forum_prj import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def index(req):
    return render(req, 'index.html')

def about(req):
    form = MessageForm(req.POST)
    if req.method == "POST":
        form = MessageForm(req.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            try: 
                send_mail(subject, body, settings.EMAIL_HOST_USER, ["fiyduzarko@gufum.com"], fail_silently=False)
                form.save()
            except Exception as err:
                print(str(err))
            return redirect('about')
    return render(req, "about.html", {"form":form})

class RegisterForm(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_message = "%(username)s was created successfully"
    template_name = "register.html"
    success_url = reverse_lazy('login')

class PostView(ListView):
    model = Post
    template_name = "index.html"
    ordering = ['-created_at']

class DetailPostView(DetailView):
    model = Post
    template_name = "detail_post.html"

# class CreatePostView(PermissionRequiredMixin, CreateView):
#     permission_required = 'service.add_post'
#     model = Post
#     template_name = "create_post.html"
#     form_class = PostForm

@login_required
@permission_required("service.add_post")
def create_post(req):
    form = PostForm()
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get("title")
            if title != "POST":
                messages.error(req, f"Something went wrong")
                return redirect('index')
            # id = form.cleaned_data.get("pk")
            messages.success(req, f"Post {title} was creates successfully")
            return redirect('index')

    return render(req, "create_post.html", {"form":form})


class UpdatePostView(PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_post'
    model = Post
    template_name = "create_post.html"
    form_class = PostForm
    
class DeletePostView(PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_post'
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('index')

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "add_comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

def upload(req):
    context = {}
    if req.method == "POST":
        upload_file = req.FILES['file']
        file = FileSystemStorage()
        name = file.save(upload_file.name, upload_file)
        context['url'] = file.url(name)
    return render(req,"upload.html", context)

def download(req):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(("Title", "Description", "Created_at"))

    for row in Post.objects.all().values_list('title', 'description', 'created_at'):
        writer.writerow(row)
    filename =str(datetime.datetime.now()) + ' ' + 'post.csv'
    response["Cotent-Discription"] = f"attachment; filename={filename}"
    return response