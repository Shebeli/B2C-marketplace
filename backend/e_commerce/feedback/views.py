from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from feedback.models import ProductComment, ProductReview
from feedback.permissions import (
    IsCommentOwner,
    IsEcomAdmin,
    IsReviewOwner,
)
from feedback.serializers import (
    ProductCommentSerializer,
    ProductReviewSerializer,
)

# Product Reviews Views


class ProductReviewList(GenericAPIView, mixins.CreateModelMixin):
    """
    GET:
    Lists all the reviews for the provided product id (paginated).
    """

    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        if not self.kwargs["pk"]:
            raise ValidationError("Product's id should be provided.")
        return super().get_queryset().filter(product=self.kwargs["pk"]).order_by("id")

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ProductReviewCreate(CreateAPIView):
    """
    POST:
    For creating a review for a product, user should be authenticated.

    If the following criteria are not met, an appropriate error will be returned:

    1) The passed in order should be either in COMPLETED or DELIVERED status.
    2) The user cannot leave out more than one review for each product.
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)

    

class ProductReviewDetail(RetrieveUpdateDestroyAPIView):
    """
    DELETE:
    Deletes the given review object.

    PUT/PATCH:
    Update the given review (fields 'product' and 'order' are not updatable, thus
    any inputted values are ignored for this fields).
    """

    permission_classes = [IsReviewOwner | IsEcomAdmin]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class CustomerProductReviews(ListAPIView):
    """
    GET:
    Lists all the reviews for the current authenticated user (paginated).
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return super().get_queryset().filter(reviewed_by=self.request.user)


# Product Comment Views


class ProductCommentCreate(CreateAPIView):
    """
    POST:
    For creating a comment for a product, user should be authenticated.

    If the following criteria are not met, an appropriate error will be returned:

    1) The user cannot leave out more than one comment for each product.
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)


class CustomerProductComments(ListAPIView):
    """
    GET:
    Lists all the comments for the current authenticated user (paginated).
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(reviewed_by=self.request.user)


class ProductCommentList(ListAPIView):
    """
    GET:
    Lists all the comments for a specific product (paginated).
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


class ProductCommentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentOwner | IsEcomAdmin]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
