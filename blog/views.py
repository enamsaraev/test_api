from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

from acc import serializers as acc_ser
from acc.models import Post, Subscription



class UserListView(generics.ListAPIView):
    """
        Shows all users
        EXAMPLE: curl http://127.0.0.1:8000/blog/users/
    """

    queryset = User.objects.all()
    serializer_class = acc_ser.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
        Shows user info only for authenticated users
        Takes user's PK
        EXAMPLE: curl http://127.0.0.1:8000/blog/users/1/
            return all posts of user with pk=1
    """

    queryset = User.objects.all()
    serializer_class = acc_ser.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostList(generics.ListAPIView):
    """
        Shows all posts
        EXAMPLE: curl http://127.0.0.1:8000/blog/posts/
    """

    queryset = Post.objects.all()
    serializer_class = acc_ser.PostSerializer


class ShowPostsByDate(generics.ListAPIView):
    """
        Shows sorted list of posts by date
        EXAMPLE: curl http://127.0.0.1:8000/blog/posts/by_date/
    """

    serializer_class = acc_ser.PostSerializer
    queryset = Post.objects.order_by('-created_at')


class PostDetail(generics.RetrieveAPIView):
    """
        Shows post info only for authenticated users
        Takes post's PK
        EXAMPLE: curl http://127.0.0.1:8000/blog/posts/1/
            return a post with pk=1
    """

    serializer_class = acc_ser.PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CreateSubscription(generics.CreateAPIView):
    """
        Create a subscription
        Available only for authenticated users
        Takes PK of user to whom the subscription will be made
        EXAMPLE: curl http://127.0.0.1:8000/blog/users/1/subscribe/
            create a subscription to user with pk=1
    """
    serializer_class = acc_ser.SubSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = acc_ser.SubSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            """Cheking for a subscription"""

            if Subscription.objects.filter(subscriber=User.objects.get(username=self.request.user),
                                           blog_author=User.objects.get(pk=self.kwargs['pk'])).exists():
                return Response(
                    {'detail': 'Подписка существует'},
                    status=status.HTTP_200_OK)
            else:
                """Creating a subscription"""

                serializer.save(subscriber=User.objects.get(username=self.request.user),
                                blog_author=User.objects.get(pk=self.kwargs['pk']))
                data['response'] = True
                return Response(data, status=status.HTTP_201_CREATED)


# Create your views here.
