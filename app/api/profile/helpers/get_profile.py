from ...helpers.serialization_errors import error_dict
from rest_framework.serializers import ValidationError
from ..models import Profile


def get_user_profile(username):
    """
    Function to get user profile
    Args:
        username (str): username
    Raises:
        ValidationError: If user profile does not exist
    Returns:
        profile (obj): user profile
    """
    try:
        # We use the `select_related` method to avoid making unnecessary
        # database calls.
        profile = Profile.objects.select_related('user').get(
            user__username=username
        )

    except Profile.DoesNotExist:
        raise ValidationError(
            error_dict['does_not_exist'].format("User profile"),
        )
    return profile
