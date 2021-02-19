from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..helpers.constants import FETCH_SUCCESS_MESSAGE, UPDATED_SUCCESS_MESSAGE
from ..helpers.pagination_helper import Pagination
from ..helpers.renderers import RequestJSONRenderer
from .helpers.get_profile import get_user_profile
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.filters import SearchFilter


class ProfileRetrieveAPIView(RetrieveAPIView):
    """
    Class that handles retrieving of user profiles
    """
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        """
        Try to retrieve the requested profile and throw an exception if the
        profile could not be found.
        Args:
            self (obj): class instance
            request (obj): request instance
            username (str): User
        Returns:
            User profile data
        """
        profile = get_user_profile(username)

        serializer = self.serializer_class(profile)
        response = {
            "message": FETCH_SUCCESS_MESSAGE.format("User Profile"),
            "profile": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class ProfileListUpdateAPIView(ListAPIView, GenericAPIView):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = ProfileSerializer
    pagination_class = Pagination
    filter_backends = (SearchFilter,)
    queryset = Profile.objects.all().order_by('first_name')
    search_fields = ('first_name', 'last_name', 'bio',
                     'user__email', 'user__username', 'phone_number',)

    @action(methods=['GET'], detail=False, url_name='Search users')
    def search(self, request, *args, **kwargs):
        """
        Search users
        """
        return super().list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Update details of the currently logged in person
        """
        data = request.data
        serializer = self.serializer_class(
            request.user.profile, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': UPDATED_SUCCESS_MESSAGE.format("Profile"),
                    'profile': serializer.data}

        return Response(response, status=status.HTTP_200_OK)
