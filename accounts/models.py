from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'profile_pictures', default='default.jpg')
    description = models.CharField(max_length=500, blank=True)
    stars = models.ManyToManyField(User, related_name="user_start", blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def created_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)