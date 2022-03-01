"""
    Serializers are used to display data with nested json responses
    EXAMPLE
            {
            "username": "tu",
            "first_name": "name",
            "last_name": "surname",
            "email": "tu@mail.com",
            "posts": [
                {
                    "title": "title",
                    "text": "text",
                    "created_at": "2022-02-21T12:24:30.040496Z"
                }
            ]
        }
    In this case the PostSerializerRead was used
"""


from django.contrib.auth.models import User
from rest_framework import serializers

from acc.models import Post, Subscription


class PostSerializerRead(serializers.ModelSerializer):
    """Serializers data from Post model for display only"""
    class Meta:
        model = Post
        fields = ['title', 'text', 'created_at']


class UserSerializerRead(serializers.ModelSerializer):
    """Serializers data from Post model for display only"""
    posts = PostSerializerRead(many=True)

    class Meta:
        model = User
        fields = ['username', 'posts']


class SubSerializerRead(serializers.ModelSerializer):
    """Serializers data from Subscription model for display only"""

    blog_author = UserSerializerRead()

    class Meta:
        model = Subscription
        fields = ['blog_author', 'date']

