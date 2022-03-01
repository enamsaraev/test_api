import time

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from acc.models import Post, Subscription
from . import views

class BlogTests(APITestCase):
    def setUp(self):
        """Creating a default user"""

        self.test_user = User.objects.create_user(
            username='somename',
            password='test_password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

    def test_show_posts(self):
        """Testing the display of posts in user acc"""

        self.client.login(username='somename', password='test_password')

        response = self.client.get(reverse('shows_users_posts'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posts_by_date(self):
        """Testing the display of posts by date"""

        for i in range(1, 6):
            Post.objects.create(
                title='title' + str(i),
                text='text',
                user=self.test_user
            )
            time.sleep(0.05)

        post = Post.objects.all().order_by('-created_at')[0]
        response = self.client.get(reverse('posts_by_date'), format='json').render()

        self.assertEqual(post.title, response.data[0]['title'])

    def test_posts_by_id(self):
        """Testing the display of post by id"""

        Post.objects.create(
            title='title_by_id',
            text='text',
            user=self.test_user
        )

        self.client.login(username='somename', password='test_password')

        post = Post.objects.get(title='title_by_id')
        response = self.client.get('/blog/posts/%s/' % (post.id), format='json')

        self.assertEqual(response.data['title'], post.title)

    def test_user_by_id(self):
        """Testing the display of user by id"""

        User.objects.create(
            username='testname',
            password='testpassword',
            first_name='name',
            last_name='last',
            email='test@mail.com'
        )

        self.client.login(username='somename', password='test_password')

        user = User.objects.get(username='testname')
        response = self.client.get('/blog/users/%s/' % (user.id), format='json')

        self.assertEqual(response.data['username'], user.username)

    def test_make_subscription(self):
        """Testing the display of subscriptions"""

        User.objects.create_user(
            username='nameofuser',
            password='password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

        test_author = User.objects.get(username='nameofuser')

        data = {
            'subscriber': self.test_user,
            'blog_author': test_author,
        }

        self.client.login(username='somename', password='test_password')

        self.client.post('/blog/users/%s/subscribe/' % (test_author.id), data, format='multipart')

        sub = Subscription.objects.order_by('-date')[0]

        self.assertEqual(sub.subscriber, self.test_user)
        self.assertEqual(sub.blog_author, test_author)




# Create your tests here.
