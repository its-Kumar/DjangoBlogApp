from django.contrib import admin

from blog.models import Post

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish', 'updated', 'draft']
    list_display_links = ['title', 'updated']
    list_filter = ['updated', 'publish', 'draft']
    ist_editable = ['draft']
    search_fields = ['title', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
