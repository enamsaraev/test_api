from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class IntegrityTest(APITestCase):
    def setUp(self):
        self.test_author = User.objects.create_user(
            username='nameofauthor',
            password='password',
            first_name='name',
            last_name='last',
            email='some@mail.com'
        )

    def test_user_registration_and_make_a_subscription(self):
        data = {
            'username': 'nameofsub',
            'password': 'password',
            'password_repeat': 'password',
            'first_name': 'name',
            'last_name': 'last',
            'email': 'some@mail.com'
        }
        registration = self.client.post(reverse('create_acc'), data, format='json')
        self.assertEqual(registration.status_code, status.HTTP_200_OK)

        self.client.login(username='nameofsub', password='password')
        data = {
            'title': 'title',
            'text': 'text'
        }
        response = self.client.post(reverse('create_post'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res = self.client.post('/blog/users/%s/subscribe/' % (self.test_author.id), format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)