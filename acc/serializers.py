from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Subscription
from blog import serializers as blog_ser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """"
        Serializes data for user registration
        Has an additional filed in default User model - password_repeat
            - If the password and password_repeat fields are different, it will not allow to create a model
            - If password length is less than 8 characters, it will not allow to create a model
    """
    password_repeat = serializers.CharField()

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'password_repeat',
                  'first_name',
                  'last_name',
                  'email']

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )

        password = self.validated_data['password']
        password_repeat = self.validated_data['password_repeat']

        if len(password) < 8:
            raise serializers.ValidationError({password: 'Пароль короткий'})

        if password != password_repeat:
            raise serializers.ValidationError({password: 'Пароли не совпадают'})

        user.set_password(password)

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializes data for displaying user data"""

    posts = blog_ser.PostSerializerRead(many=True)

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'posts']


class PostSerializer(serializers.ModelSerializer):
    """Serializes data for displaying post data"""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['title', 'text', 'user', 'created_at']


class CreatePostSerializer(serializers.ModelSerializer):
    """Serializes data for creating a Post model"""
    class Meta:
        model = Post
        fields = ['title', 'text']
        extra_kwargs = {
            'user': {'read_only': True}
        }


class SubSerializer(serializers.ModelSerializer):
    """Serializes data for creating a subscription model"""

    class Meta:
        model = Subscription
        fields = ''
        extra_kwargs = {
            'subscriber': {'read_only': True},
            'blog_author': {'read_only': True}
        }




