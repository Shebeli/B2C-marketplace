import pytest

from feedback.serializers import ProductCommentSerializer, ProductReviewSerializer


@pytest.mark.django_db
def test_review_create_serializer():
    