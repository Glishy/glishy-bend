from app.api.helpers.renderers import RequestJSONRenderer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE
from .serializers import LoginSerializer, RegistrationSerializer
from rolepermissions.roles import assign_role


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Handle user Signup
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assign_role(serializer.instance, 'audience_member')

        response = {'message': SIGNUP_SUCCESS_MESSAGE,
                    'user': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView,):
    # Login user class
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        response = {'user': serializer.data}
        return Response(response, status=status.HTTP_200_OK)
