from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=220, verbose_name='Sarlavha')
    content = RichTextUploadingField('Matn')
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    views = models.IntegerField(default=0, null=True, blank=True)
    tags = TaggableManager(help_text="taglarni vergul(,) bilan ajratib yozing!", verbose_name='taglar')
    slug = models.SlugField(max_length=200, null=True, verbose_name='URL') 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[:50]