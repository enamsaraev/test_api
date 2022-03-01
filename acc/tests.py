from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

from .models import Subscription


class AccTest(APITestCase):
    def setUp(self):
        """Creating a default user"""

        self.test_user = User.objects.create_user(
            username='somename',
            password='test_password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

    def test_create_acc(self):
        """Testing account creation"""

        data = {
            'username': 'nameofuser',
            'password': 'password',
            'password_repeat': 'password',
            'first_name': 'name',
            'last_name': 'last',
            'email': 'some@mail.com'
        }
        response = self.client.post(reverse('create_acc'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_acc_with_unavailable_pass(self):
        """Testing account creation with wrong data"""

        data = {
            'username': 'name',
            'password': 'wer',
            'password_repeat': 'werrr',
            'first_name': 'some_name',
            'last_name': 'some_pass',
            'email': 'somemail@mail.com'
        }
        response = self.client.post(reverse('create_acc'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_from_not_authorized(self):
        """Testing post creation by an unauthorized user"""

        data = {
            'title': 'title',
            'text': 'text'
        }
        response = self.client.post(reverse('create_post'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self):
        """Testing post creation"""

        self.client.login(username='somename', password='test_password')
        data = {
            'title': 'title',
            'text': 'text'
        }
        response = self.client.post(reverse('create_post'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_my_subs_no_authorized(self):
        """Testing the display of the list of subscription for no authorized users"""

        test_author = User.objects.create_user(
            username='nameofuser',
            password='password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

        Subscription.objects.create(
            subscriber=self.test_user,
            blog_author=test_author
        )

        response = self.client.get(reverse('users_subscriptions'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_subs(self):
        """Testing the display of the list of subscription for no authorized users"""

        test_author = User.objects.create_user(
            username='nameofuser',
            password='password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

        Subscription.objects.create(
            subscriber=self.test_user,
            blog_author=test_author
        )
        self.client.login(username='somename', password='test_password')
        self.client.get(reverse('users_subscriptions'), format='multipart')

        sub = Subscription.objects.filter(subscriber=self.test_user)[0]
        self.assertEqual(sub.subscriber, self.test_user)
        self.assertEqual(sub.blog_author, test_author)




# Create your tests here.
