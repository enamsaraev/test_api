from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User,
                             related_name='posts',
                             on_delete=models.CASCADE,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    """
        Subscription model

        -blog_author: the one the user subscribe to
    """
    subscriber = models.ForeignKey(User,
                                   related_name='sub',
                                   on_delete=models.CASCADE,
                                   null=True)
    blog_author = models.ForeignKey(User,
                                    related_name='author',
                                    on_delete=models.CASCADE,
                                    null=True)
    date = models.DateTimeField(auto_now_add=True)



# Create your models here.
