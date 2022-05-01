from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User
from .utils import get_page_obj

POSTS_PER_PAGE = 10


def index(request):
    """Главная страница со списком постов."""
    context = {
        'page_obj': get_page_obj(request, Post.objects.all(), POSTS_PER_PAGE),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страниа со списком постов группы."""
    context = {
        'group': get_object_or_404(Group, slug=slug),
        'page_obj': get_page_obj(request, group.posts.all(), POSTS_PER_PAGE),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница с постами пользователя."""
    context = {
        'author': get_object_or_404(User, username=username),
        'page_obj': get_page_obj(request, user.posts.all(), POSTS_PER_PAGE),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница отдельного поста."""
    context = {
        'post': get_object_or_404(Post, id=post_id),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})

    post = form.instance
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    form = PostForm(data=request.POST or None, instance=post)
    if not form.is_valid():
        context = {
            'form': form,
            'is_edit': True,
        }
        return render(request, 'posts/create_post.html', context)

    form.save()
    return redirect('posts:post_detail', post_id)
