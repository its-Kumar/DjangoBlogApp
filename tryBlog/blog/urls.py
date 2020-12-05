from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='list'),
    path('create/', views.post_create, name='create'),
    path('<str:slug>/', views.post_detail, name='detail'),
    path('<str:slug>/edit/', views.post_update, name='update'),
    path('<str:slug>/delete/', views.post_delete, name='delete'),

]
