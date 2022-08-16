from django import forms

from taggit.forms import TagWidget
from .models import Comment, Post




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'tags':TagWidget(),
        }
        exclude = ['author', 'likes', 'views', 'slug']
