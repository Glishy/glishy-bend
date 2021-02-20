
""" Serializers Configuration here """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

from ..helpers.serialization_errors import error_dict
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    """Serializers registration requests and creates a new user."""

    # Ensure email is provided and is unique
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all_with_deleted(),
                message=error_dict['already_exist'].format("Email"),
                lookup="iexact"
            )
        ],
        error_messages={
            'required': error_dict['required'],
        }
    )
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the user.
    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=True,
        allow_null=False,
        write_only=True,
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format("Password", "8"),
            'max_length': 'Password cannot be more than 30 characters',
            'invalid': error_dict['invalid_password'],
        }
    )
    # Ensure that the first_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all_with_deleted(),
                message=error_dict['already_exist'].format("Username"),
                lookup="iexact"
            ),
        ],
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Username')
        }
    )

    # Ensure that the last_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    # The user should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(read_only=True)

    class Meta:

        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    @staticmethod
    def create(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**self)


class LoginSerializer(serializers.Serializer):

    """Login serializer Class"""
    email = serializers.EmailField(required=True,
                                   allow_null=False,
                                   error_messages={
                                       'required': error_dict['required'], })
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     allow_null=False,
                                     error_messages={
                                         'required': error_dict['required'], })
    username = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    roles = serializers.ListField(read_only=True)

    @staticmethod
    def validate(data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email')
        password = data.get('password')

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(email=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(error_dict['user_not_found'])

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'roles': user.roles,
            'token': user.token,
        }
