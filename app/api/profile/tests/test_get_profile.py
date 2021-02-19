from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import status

from ...helpers.serialization_errors import error_dict
from .base_test import ProfileTestBaseCase


class GetUserProfileTest(ProfileTestBaseCase):

    def test_get_user_profile_succeeds(self):
        """Test profile can be fetched successfully"""
        response = self.get_profile_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('image', response.data['profile'])
        self.assertIn('username', response.data['profile'])

    def test_get_non_existing_user_profile_fails(self):
        """Test get non existant profile fails"""
        response = self.get_profile_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(error_dict['does_not_exist'].format("User profile"), str(response.data))

    def test_list_user_profiles_succeeds(self):
        """Test profiles can be fetched successfully"""
        self.get_profile_successfully()
        response = self.client.get(self.list_update_profile_url,
        HTTP_AUTHORIZATION='bearer {}'.format(
            self.login_user_successfull().data['user']['token']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['rows'], list)
        self.assertIn('totalRecords', response.data['paginationMeta'])
