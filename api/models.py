from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import random
import string

def gen_rand_str():
    return ''.join([random.choice(string.ascii_letters) for _ in range(15)])

class ChatMessage(models.Model):
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, default=gen_rand_str)
    picture = models.TextField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
