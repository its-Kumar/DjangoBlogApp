from django import forms
from pagedown.widgets import PagedownWidget

from blog.models import Post


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    # content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'draft', 'publish']
