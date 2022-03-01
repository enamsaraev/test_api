from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response

from .models import Post, Subscription
from blog import serializers as blog_ser
from acc import serializers


class CreateProfile(generics.CreateAPIView):
    """
        Profile creation
        EXAMPLE: curl http://127.0.0.1:8000/acc/createacc/
    """

    queryset = User.objects.none()
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """The received data is checked in UserRegistrationSerializer"""

        serializer = serializers.UserRegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = serializer.errors
            return Response(data)


class CreatePostView(generics.CreateAPIView):
    """
        Account creation
        Only for authenticated users
        EXAMPLE: curl http://127.0.0.1:8000/acc/createpost/
            data '{"title":"title","text":"text"}
    """
    serializer_class = serializers.CreatePostSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        """The received data is checked in CreatePostSerializer"""

        serializer = serializers.CreatePostSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            serializer.save(user=User.objects.get(username=self.request.user))
            data['response'] = True
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            Response({'response': 'Необходима авторизация'}, status=status.HTTP_401_UNAUTHORIZED)


class ShowMyPostsView(generics.ListAPIView):
    """
        Return the list of user's posts
        Only for authenticated users
        EXAMPLE: curl http://127.0.0.1:8000/acc/myposts/
    """

    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=User.objects.get(username=self.request.user))


class ShowMySubscriptions(generics.ListAPIView):
    """
        Account creation
        Only for authenticated users
        EXAMPLE: curl http://127.0.0.1:8000/acc/mysub/
    """

    serializer_class = blog_ser.SubSerializerRead
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


# Create your views here.
