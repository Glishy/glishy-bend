from rest_framework.reverse import reverse as api_reverse
from ..models import Profile
from ...authentication.tests.base_test import TestBaseCase

class ProfileTestBaseCase(TestBaseCase):
    def setUp(self):
        """
        Method for setting up user
        """
        super().setUp()
        self.list_update_profile_url = api_reverse('profile:list-update-profile')

        self.valid_profile ={
            'first_name': 'jane',
            'last_name': 'Doe',
            'bio': 'my profile',
            'image': 'http://image.png',
            'facebook_account': 'http://facebook-account.com',
            'twitter_account': 'http://twitter-account.com',
            'instagram_account': 'http://instagram-account.com',
            'twitch_account': 'http://twitch-account.com',
            'phone_number': "+25412534545"
        }
        self.invalid_profile_data ={
            'first_name': '!!!!jane',
            'last_name': '!!!Doe',
            'image': 'http://image',
            'facebook_account': 'http://facebook-account',
            'twitter_account': 'http://twitter-account',
            'instagram_account': 'http://instagram-account',
            'twitch_account': 'http://twitch-account',
            'phone_number': "+25"
        }


    def get_profile_successfully(self):
        """
        method to get user profile
        """
        user = self.signup_user()
        url = api_reverse('profile:retrieve-profile', kwargs={"username":user.username})
        response = self.client.get(url)
        return response

    def get_profile_fails(self):
        """
        get non existing user profile
        """
        url = api_reverse('profile:retrieve-profile', kwargs={"username":"user.username"})
        response = self.client.get(url)
        return response

    # def login_user_fails(self):
    #     """
    #     method to try login a user with invalid data
    #     """
    #     response = self.client.post(self.login_url,
    #                                 self.invalid_user_login_details, format='json')
    #     return response

    # def signup_user(self):
    #     """
    #     successfully signup user
    #     """
    #     self.client.post(
    #         self.signup_url, self.valid_user, format='json')
    #     return User.objects.get(email=self.valid_user['email'])

    # def activated_user(self):
    #     """
    #     create an active user
    #     """
    #     user = self.signup_user()
    #     user.is_active = True
    #     user.save()
    #     return user

