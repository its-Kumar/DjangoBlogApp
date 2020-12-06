from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import PostModelForm
from blog.models import Post
from comments.forms import CommentForm
from comments.models import Comment

from .utils import get_read_time

# Create your views here.


def post_list(request):
    query_set = Post.objects.active()
    paginator = Paginator(query_set, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "posts": posts
    }
    return render(request, 'blog/list.html', context=context)


@login_required
def post_create(request):
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'successfully created')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'creation failed')
    context = {
        "form": form
    }
    return render(request, 'blog/form.html', context=context)


def post_detail(request, slug):
    # post = Post.objects.get(slug=slug)
    post = get_object_or_404(Post, slug=slug)
    if post.draft:
        if post.user != request.user:
            raise Http404
    print(get_read_time(post.get_markdown()))
    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }
    parent_obj = None
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        try:
            parent_id = int(request.POST.get("parent_id"))
        except Exception:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    # comments = Comment.objects.filter_by_instance(post)
    comments = post.comments
    context = {
        "post": post,
        "comment_form": form,
        "comments": comments,
        "parent": parent_obj,
    }
    return render(request, 'blog/detail.html', context=context)


@login_required
def post_update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    form = PostModelForm(request.POST or None,
                         request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'successfully saved')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'updation failed')
    context = {
        "form": form,
        "title": instance.title
    }
    return render(request, 'blog/form.html', context=context)


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'successfully deleted')
    return redirect('blog:list')
