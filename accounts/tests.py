from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from accounts.serializers import AccountSerializer
from accounts.views import AccountView

User = get_user_model()


class AccountSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            'username': 'bdksj1',
            'email': 'testemamil@email.co',
            'password': 'ajdhkn123213f',
        }

        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_username(self):
        data = {
            'username': '%%2ccf123',
            'email': 'testemamil@email.co',
            'password': 'ajdhkn123213f',
        }

        serializer = AccountSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_invalid_email(self):
        data = {
            'username': 'user1234',
            'email': 'testdsil.co',
            'password': 'ajdhkn123213f',
        }

        serializer = AccountSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_invalid_password(self):
        data = {
            'username': 'user1234',
            'email': 'testemamil@email.co',
            'password': 'a',
        }

        serializer = AccountSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_missing_email(self):
        data = {
            'username': 'user1234',
            'password': 'adeferh7863546',
        }

        serializer = AccountSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)


class AccountTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.location = "/api/account/"

    def test_signup(self):
        request = self.factory.post(
            self.location,
            {
                'username': 'bdksj1',
                'email': 'testemamil@email.co',
                'password': 'ajdhkn123213f',
            },
            content_type='application/json',
        )

        response = AccountView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testDuplicateUsernameSignup(self):
        User.objects.create_user(username="abcd123", email="email@email.com", password="djksldksld")
        request = self.factory.post(
            self.location,
            {
                'username': 'abcd123',
                'email': 'testemail@email.com',
                'password': 'dljkwldkc',
            },
            content_type='application/json',
        )

        response = AccountView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testAccountGet(self):
        user = User.objects.create_user(username="abcd123", email="email@emil.com", password="djksldksld")
        request = self.factory.get(
            self.location,
            content_type='application/json',
        )
        force_authenticate(request, user)

        response = AccountView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testAccountUpdate(self):
        user = User.objects.create_user(username="abcd123", email="email@emil.com", password="djksldksld")
        request = self.factory.get(
            self.location,
            {
                'bio': "dsjkadjsldkjas",
                'username': "abcd12345"
            },
            content_type='application/json',
        )
        force_authenticate(request, user)

        response = AccountView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
