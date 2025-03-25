import factory
import pytest
from ecom_user.models import EcomUser
from ecom_user_profile.tests.profile_factory import CustomerFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from order.models import Order
from order.tests.order_factory import OrderFactory, OrderItemFactory
from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    SubCategoryBreadCrumb,
    Tag,
    TechnicalDetail,
)
from product.tests.product_factory import ProductFactory, ProductVariantFactory

from feedback.models import ProductReview, ProductComment
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


@pytest.mark.django_db
def test_review_serializer_creation():
    customer = CustomerFactory()
    order = OrderFactory(customer=customer)
    order_item = OrderItemFactory(order=order)
    product = order_item.product_variant.product

    data = {
        "product": product.id,
        "reviewed_by": customer.id,
        "order": order.id,
        "rating": 5,
        "title": "Sample title",
        "description": "Sample description",
    }

    serializer = ProductReviewSerializer(data=data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    assert data == {
        "product": obj.product.id,
        "reviewed_by": obj.reviewed_by.id,
        "order": obj.order.id,
        "rating": obj.rating,
        "title": obj.title,
        "description": obj.description,
    }


@pytest.mark.django_db
def test_review_serializer_update():
    product = ProductFactory()
    variant = ProductVariantFactory(product=product)
    order = OrderFactory()
    OrderItemFactory.create(product_variant=variant, order=order)
    review = ProductReviewFactory(order=order, product=product)
    new_data = {
        "product": review.product.id,
        "reviewed_by": review.reviewed_by.id,
        "rating": 1,
        "title": "New title",
        "description": "New description",
    }

    serializer = ProductReviewSerializer(review, data=new_data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    assert new_data == {
        "product": obj.product.id,
        "reviewed_by": obj.reviewed_by.id,
        "rating": obj.rating,
        "title": obj.title,
        "description": obj.description,
    }
