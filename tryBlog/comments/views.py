from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Comment

# Create your views here.


def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)
    content_obj = comment.content_object
    content_id = comment.content_object.id
    initial_data = {
        "content_type": content_obj.get_content_type,
        "object_id": content_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
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
    context = {
        "comment": comment,
        "comment_form": form,
    }
    return render(request, 'comments/thread.html', context=context)


@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user != request.user:
        response = HttpResponse("You do not have the permission to do this.")
        response.status_code = 403
        return response

    if request.POST:
        comment.delete()
        messages.success(request, "The comment has been Deleted...")
        return redirect('blog:list')
    context = {
        "comment": comment,
    }
    return render(request, 'comments/delete.html', context=context)
