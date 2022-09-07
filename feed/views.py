from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView

from .models import Post, Comment


@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        following = user.profile.following.all()
        return self.model.objects.filter(Q(author__profile__in=following) | Q(author=user))


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

@login_required
def add_comment(request, pk):
    if request.method != 'POST':
        return redirect('post-detail', pk=pk)
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    try:
        comment = request.POST.get('comment-input')
        post.comment_set.create(author=user, comment=comment)
        return render(request, 'feed/comment-section.html', {'post': post})
        # return JsonResponse({"success": True}, status=200)
        # return redirect('post-detail', pk=pk)
    except (KeyError):
        return JsonResponse({"success": False}, status=400)


@login_required
def like_post(request, pk):
    if request.method != 'POST':
        return redirect('post-detail', pk=pk)
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if post.likes.contains(user):
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return render(request, 'feed/like-section.html', {'post': post})


@login_required
def create_post(request):
    if request.method != 'POST':
        raise Http404
    try:
        image = request.FILES['image']
        caption = request.POST['caption']
        user = request.user
        user.post_set.create(caption=caption, image=image)
        return redirect('feed-home')
    except (KeyError):
        return redirect('feed-home')


@login_required
def delete_post(request, pk):
    if request.method != 'POST':
        return redirect('post-detail', pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('feed-home')
    return redirect('post-detail', pk=pk)
