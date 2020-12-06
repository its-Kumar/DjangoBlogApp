"""tryBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls import include, path

from searches.views import search_view


def home(request):
    return HttpResponseRedirect("/posts/", "<h1>Hello</h1>from: <p>Kumar Shanu</p>")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pagedown.urls')),
    path('', home, name="home"),
    path('posts/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    path("search/", search_view),
    path("accounts/", include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
