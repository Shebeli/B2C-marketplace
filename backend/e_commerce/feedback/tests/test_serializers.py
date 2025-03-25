import factory
import pytest
from ecom_user.models import EcomUser
from factory import SubFactory
from factory.django import DjangoModelFactory
from order.models import Order
from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    SubCategoryBreadCrumb,
    Tag,
    TechnicalDetail,
)
from product.tests.product_factory import ProductFactory

from feedback import models
from feedback.serializers import ProductReviewSerializer
from feedback.tests.feedback_factory import ProductReviewFactory


@pytest.mark.django_db
def test_review_serializer_representation():
    review = ProductReviewFactory.create()
    serializer = ProductReviewSerializer(review)
    assert serializer.data == {
        "id": review.id,
        "product": review.product.id,
        # "order": review.order.id, this is a write only field!
        "reviewed_by": review.reviewed_by.id,
        "rating": 3,
        "title": review.title,
        "description": review.description,
    }
