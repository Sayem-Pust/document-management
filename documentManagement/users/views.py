from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework import generics, permissions
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, response


class RegistrationView(generics.CreateAPIView):
    """ User Registration with username, email, first name, last name, password, confirm password and
     is superuser(optional) on the top of django build in authentication system """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
    """ User Login with username or email and password and get a access token for authentication"""
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        password = request.data.get('password')
        identifier = request.data.get('identifier')
        user_instance = User.objects.filter(
            Q(email=identifier) | Q(username=identifier)).first()
        if user_instance is not None:
            if user_instance.check_password(password):
                refresh = RefreshToken.for_user(user_instance)
                return response.Response(
                    {
                        'message': 'login successful',
                        'data': {
                            'user': RegistrationSerializer(user_instance).data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return response.Response(
                    {
                        'message': 'Invalid Credential',
                        'is_active': True
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(
                {
                    'message': 'Invalid Credential',
                    'is_active': True
                }, status=status.HTTP_400_BAD_REQUEST
            )





