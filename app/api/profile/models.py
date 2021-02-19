
from django.db import models
from ..models import BaseModel


class Profile(BaseModel):
    """
    User profile Model
    """
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True, db_index=True)
    image = models.URLField(blank=True)
    phone_number = models.CharField(db_index=True,
                                    max_length=15, blank=True)
    first_name = models.CharField(db_index=True, max_length=20, unique=False)

    last_name = models.CharField(db_index=True, max_length=20, unique=False)
    facebook_account = models.URLField(blank=True, null=True)
    twitter_account = models.URLField(blank=True, null=True)
    instagram_account = models.URLField(blank=True, null=True)
    twitch_account = models.URLField(blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of this `Profile`.

        This string is used when a `Profile` is printed in the console.
        """
        return f"<Profile - {self.user.email} >"

    @property
    def profile_type(self):
        """
        Function to get user profile type
        Args:
            self (obj): class instance
        Returns:
            (str): User roles
        """
        roles = self.user.roles

        return "content_creator" if "content_creator" \
            in roles else "audience_member"
