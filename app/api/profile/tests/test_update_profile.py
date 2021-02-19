from app.api.helpers.constants import UPDATED_SUCCESS_MESSAGE
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import status

from ...helpers.serialization_errors import error_dict
from .base_test import ProfileTestBaseCase


class UpdateUserProfileTest(ProfileTestBaseCase):

    """
    User profile update test cases
    """

    def test_user_profile_update_succeed(self):
        """
        Test API can successfully update a user profile
        """
        token = self.login_user_successfull().data['user']['token']
        response = self.client.patch(
            self.list_update_profile_url, self.valid_profile, HTTP_AUTHORIZATION='bearer {}'.format(token), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], UPDATED_SUCCESS_MESSAGE.format("Profile"))

    def test_invalid_profile_data_update_fails(self):
        """
        Test API fails to update profile due to invalid data
        """
        token = self.login_user_successfull().data['user']['token']
        response = self.client.patch(
            self.list_update_profile_url, self.invalid_profile_data, HTTP_AUTHORIZATION='bearer {}'.format(token), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['errors'], list)

    # def test_empty_fields_signup_fails(self):
    #     """
    #     Test API fails to register a new user due to
    #     empty fields
    #     """
    #     response = self.client.post(
    #         self.signup_url, self.missing_user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertIsInstance(response.data['errors'], list)
