from django.shortcuts import render

from blog.models import Post
from comments.models import Comment

from .models import SearchQuery

# Create your views here.


def search_view(request):
    query = request.GET.get("q", None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    post_list = []
    comment_list = []
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        post_list = Post.objects.search(query=query)
        comment_list = Comment.objects.search(query=query)
    context = {
        "query": query,
        "post_list": post_list,
        "comment_list": comment_list,
    }

    return render(request, "searches/view.html", context)
