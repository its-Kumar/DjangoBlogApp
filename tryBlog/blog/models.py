from comments.models import Comment
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

# Create your models here.


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def search(self, query):
        return super(PostManager, self).filter(Q(title__contains=query) | Q(content__contains=query))




def upload_location(instance, filename):
    return f"{instance.id}/{filename}"


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_location, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-publish', '-updated', '-timestamp']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse('blog:update', kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse('blog:delete', kwargs={"slug": self.slug})

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def pre_save_post_reciever(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = f"{slug}-{instance.id}"
    instance.slug = slug

pre_save.connect(pre_save_post_reciever, sender=Post)
