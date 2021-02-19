
import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.timezone import datetime, timedelta
from softdelete.models import SoftDeleteManager
from rolepermissions.roles import get_user_roles

from ..models import BaseModel


class UserManager(BaseUserManager, SoftDeleteManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.pop('password', '')
        email = kwargs.pop('email', '')
        is_staff = kwargs.pop('is_staff', False)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser powers.

        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        password = kwargs.pop('password', '')
        email = kwargs.pop('email', '')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Each `User` needs a human-readable unique identifier that we can use to
    represent the `User` in the UI. We want to index this column in the
    database to improve lookup performance."""

    username = models.CharField(null=False,
                                db_index=True, max_length=255,
                                unique=True, blank=False)

    email = models.EmailField(db_index=True, unique=True, blank=False)

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return f"<User - {self.email} >"

    @property
    def roles(self):
        roles = []
        for i in get_user_roles(self):
            roles.append(i.get_name())
        return roles

    @property
    def token(self):
        """
        This method generates and returns a string of the token generated.
        """
        date = datetime.now() + timedelta(hours=settings.TOKEN_EXP_TIME)

        payload = {
            'email': self.email,
            'exp': int(date.strftime('%s')),
            'id': self.id,
            "username": self.username
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token
