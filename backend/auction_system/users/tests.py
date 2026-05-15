from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserCreateViewTest(APITestCase):

    def test_create_user(self): 

        data = {
            "name": "testuser",
            "email": "test@example.com",
        }

        response = self.client.post(
            "/api/users/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_user_without_name(self):

        data = {
            "name": "",
            "email": "test@example.com"
        }

        response = self.client.post(
            "/api/users/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_user_with_wrong_email(self):

        data = {
            "name": "testuser",
            "email": "not-an-email"
        }

        response = self.client.post(
            "/api/users/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
