from backend.e_commerce.feedback.models import ProductComment, ProductReview
from backend.e_commerce.feedback.permissions import (
    IsCommentOwner,
    IsEcomAdmin,
    IsReviewOwner,
)
from backend.e_commerce.feedback.serializers import (
    ProductCommentSerializer,
    ProductReviewSerializer,
)
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class ProductReviewList(GenericAPIView, mixins.CreateModelMixin):
    """
    GET:
    Lists all the reviews for a given product id.
    The id of product should be provided in the URL.

    POST:
    For creating a review for a product, user should be authenticated.

    If the following criteria are not met, an appropriate error will be returned:

    1) The user should have an order either in COMPLETED or DELIVERED status with
    the given product existing in the order items.

    2) The user also cannot leave out more than one review for each product.

    The review is specific to a product, not its variants.
    """

    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        if not self.kwargs["pk"]:
            raise ValidationError("Product's id should be provided.")
        return super().get_queryset().filter(product=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)


class ProductReviewDetail(
    GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    """
    Allows the owner of the given review object to either edit or delete it.

    DELETE:
    Deletes the given review

    PUT/PATCH:
    Update the given review (fields 'product' and 'order' are not updatable, thus
    any inputted values are ignored for this fields)
    """

    permission_classes = [IsReviewOwner | IsEcomAdmin]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class EcomUserProductReviews(GenericAPIView, mixins.ListModelMixin):
    """
    Lists all the reviews for the current authenticated user.
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return super().get_queryset().filter(reviewed_by=self.request.user)


class ProductCommentList(
    GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin
):
    """
    Requires the current user to be authenticated. both create and list will
    use the current authenticated user.

    POST:
    Create a product comment (with constraint of only one comment per product).

    GET:
    Lists all comments for current authenticated user.
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(commented_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(commented_by=self.request.user)


class ProductCommentDetail(
    GenericAPIView,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsCommentOwner | IsEcomAdmin]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
