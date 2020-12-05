from django.urls import path

from comments.views import comment_delete, comment_thread

urlpatterns = [
    path('<int:id>/', comment_thread, name="thread"),
    path('<int:id>/delete/', comment_delete, name="delete"),
]
