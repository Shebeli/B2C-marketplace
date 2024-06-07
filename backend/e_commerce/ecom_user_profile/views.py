from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecom_user_profile.models import CustomerProfile
from ecom_user_profile.serializers import CustomerProfileSerializer
from ecom_user.authentication import EcomUserJWTAuthentication


class CustomerProfileAPIView(APIView):
    "Retrieve or update current authenticated user's customer profile"
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomerProfile, user=self.request.user)

    def get(self, request, format=None):
        "Returns the current authenticated user customer profile"
        instance = self.get_object()
        serializer = CustomerProfileSerializer(instance)
        return Response(serializer.data)

    def patch(self, request, format=None):
        "Partial update the current authenticated user profile"
        instance = self.get_object()
        serializer = CustomerProfileSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)