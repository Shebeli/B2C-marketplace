from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

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


class ProductReviewList(ListAPIView):
    """
    GET:
    Lists all the reviews for the provided product id (paginated).
    """

    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        if not self.kwargs["pk"]:
            raise ValidationError("Product's id should be provided.")
        return (
            super()
            .get_queryset()
            .filter(product=self.kwargs["pk"])
            .order_by("created_at")
        )


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
        return (
            super()
            .get_queryset()
            .filter(reviewed_by=self.request.user)
            .order_by("created_at")
        )


# Product Comment Views


class ProductCommentCreate(CreateAPIView):
    """
    POST:
    For creating a comment for a product, user should be authenticated.

    If the following criteria are not met, an appropriate error will be returned:

    1) The user cannot leave out more than one comment for each product.
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def perform_create(self, serializer):
        serializer.save(commented_by=self.request.user)


class CustomerProductComments(ListAPIView):
    """
    GET:
    Lists all the comments for the current authenticated user (paginated).
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(commented_by=self.request.user)
            .order_by("created_at")
        )


class ProductCommentList(ListAPIView):
    """
    GET:
    Lists all the comments for a specific product (paginated).
    """

    permission_classes = [IsAuthenticated]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def get_queryset(self):
        if not self.kwargs["pk"]:
            raise ValidationError("Product's id should be provided.")
        return (
            super()
            .get_queryset()
            .filter(product=self.kwargs["pk"])
            .order_by("created_at")
        )


class ProductCommentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentOwner | IsEcomAdmin]
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
