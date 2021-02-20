""" Serializers Configuration here """
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile
from ..helpers.serialization_errors import error_dict


class ProfileSerializer(serializers.ModelSerializer):
    """
    User profile serializer
    """
    username = serializers.CharField(source='user.username', read_only=True)
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    phone_number = serializers.RegexField(
        regex='^(?:\B\+ ?254|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?',
        required=False,
        allow_blank=True,
        min_length=10,
        max_length=15,
        validators=[
            UniqueValidator(
                queryset=Profile.objects.all(),
                message=error_dict['already_exist'].format("Phone number"),
            )],
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format(
                "Phone number",
                "10"),
            'max_length': error_dict['max_length'].format(
                "Phone number",
                "15"),
            'invalid': error_dict['invalid_phone_no']})
    first_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        required=False,
        allow_blank=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('First name')
        })

    last_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        required=False,
        allow_blank=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Last name')
        })
    facebook_account = serializers.URLField(allow_blank=True, required=False)
    twitter_account = serializers.URLField(allow_blank=True, required=False)
    instagram_account = serializers.URLField(allow_blank=True, required=False)
    twitch_account = serializers.URLField(allow_blank=True, required=False)
    profile_type = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'twitch_account', 'image',
                  'phone_number', 'bio', 'facebook_account', 'instagram_account',
                  'twitter_account', 'profile_type',)

    @staticmethod
    def get_image(obj):
        """
        Function to get user image or return a default image if none exist
        Args:
            obj (obj): Profile instance
        Returns:
            (str): user image
        """
        if obj.image:
            return obj.image
        return settings.DEFAULT_USER_IMAGE
