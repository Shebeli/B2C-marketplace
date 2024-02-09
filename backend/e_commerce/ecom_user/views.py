from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EcomUser
from .serializers import UserSerializer, UpdatePhoneSerializer, CreateUserSerializer, ChangePasswordSerializer



class EcomUserViewSet(viewsets.ViewSet):
    """
    Provides the following actions:
    - Sign up, if succesful return a token pair.
    - Reset password, either by granting the access or generating a reset password link.
    - Retrieve profile using request.user
    - Edit profile using request.user
    """
    
    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(access),
        }, status=status.HTTP_201_CREATED)
        
    # @action(detail=True, )