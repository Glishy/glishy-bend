from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ..models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.login_url = api_reverse('authentication:user-login')
        self.signup_url = api_reverse('authentication:user-signup')

        self.valid_user = {
            'username': 'jDoe',
            'email': 'jane@doe.com',
            'password': 'janeDoe@123'
        }
        self.missing_user_data = {
            'username': '',
            'email': '',
            'password': '',
        }
        self.invalid_user_data = {
            'email': 'janedoe.com',
            'password': 'jane',
            'username': "&&&&&&"
        }
        self.invalid_user_login_details = {
            'email': 'janee@doe.com',
            'password': 'janeDoe@123'
        }

        self.expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imhlc2JvbmtpcHRvbzU2MDBAZ21haWwuY29tIiwiZXhwIjoxNTc0MzQ4MjE3LCJpZCI6Ii1MdThKRi1wZHZuWnp0WVFKTG9wIn0.XvopBzm6J1wIbDS7OozRtoWkG7D6xCeOFWJP5VUx3PI"

    def login_user_successfull(self):
        """
        methid to login user
        """
        self.activated_user()
        response = self.client.post(self.login_url,
                                    self.valid_user, format='json')
        return response

    def login_user_fails(self):
        """
        method to try login a user with invalid data
        """
        response = self.client.post(self.login_url,
                                    self.invalid_user_login_details, format='json')
        return response

    def signup_user(self):
        """
        successfully signup user
        """
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        return User.objects.get(email=self.valid_user['email'])

    def activated_user(self):
        """
        create an active user
        """
        user = self.signup_user()
        user.is_active = True
        user.save()
        return user

