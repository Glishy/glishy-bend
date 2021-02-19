from rest_framework import status
from .base_test import TestBaseCase
from ...helpers.constants import SIGNUP_SUCCESS_MESSAGE


class AuthenticationTest(TestBaseCase):
    """
    User authentication test cases
    """

    def test_user_signup_succeed(self):
        """
        Test API can successfully register a new user
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], SIGNUP_SUCCESS_MESSAGE)

    def test_user_signup_missing_fields_fails(self):
        """
        Test API fails to register a new user due to
        invalid data
        """
        response = self.client.post(self.signup_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)

        self.assertIsInstance(response.data['errors'], list)

    def test_invalid_user_data_signup_fails(self):
        """
        Test API fails to register a new user due to
        missing fields
        """
        response = self.client.post(
            self.signup_url, self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['errors'], list)

    def test_empty_fields_signup_fails(self):
        """
        Test API fails to register a new user due to
        empty fields
        """
        response = self.client.post(
            self.signup_url, self.missing_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['errors'], list)
