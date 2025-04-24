from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from ecom_core.exceptions.order import BaseOrderError


def order_exception_handler(exc, content):
    response = exception_handler(exc, content)
    
    if isinstance(exc, BaseOrderError):
        return Response({"error": exc.as_dict()}, status=status.HTTP_400_BAD_REQUEST)
    
    return response
    
    
