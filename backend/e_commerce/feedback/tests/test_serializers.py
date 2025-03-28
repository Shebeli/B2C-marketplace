from datetime import datetime, timedelta, timezone

import pytest
from ecom_user_profile.tests.profile_factory import CustomerFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from product.tests.product_factory import ProductFactory, ProductVariantFactory

from feedback.serializers import ProductCommentSerializer, ProductReviewSerializer
from feedback.tests.feedback_factory import ProductCommentFactory, ProductReviewFactory

# ------ Review Serializer -------
# Note that date time fields are not a matter of importance to get asserted
# with some expected value


@pytest.mark.django_db
def test_review_serializer_representation():
    review = ProductReviewFactory.create()
    serializer = ProductReviewSerializer(review)
    assert serializer.data == {
        "id": review.id,
        "product": review.product.id,
        "reviewed_by": {
            "id": review.reviewed_by.id,
            "full_name": review.reviewed_by.full_name,
            "profile_picture": None,
        },
        "rating": 3,
        "title": review.title,
        "description": review.description,
        "created_at": serializer.data["created_at"],
        "updated_at": serializer.data["updated_at"],
    }


@pytest.mark.django_db
def test_review_serializer_creation():
    customer = CustomerFactory()
    order = OrderFactory(customer=customer)
    order_item = OrderItemFactory(order=order)
    product = order_item.product_variant.product

    data = {
        "product": product.id,
        "order": order.id,
        "rating": 5,
        "title": "Sample title",
        "description": "Sample description",
    }

    serializer = ProductReviewSerializer(data=data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save(reviewed_by=customer)
    expected_data = {
        "product": obj.product.id,
        "order": obj.order.id,
        "rating": obj.rating,
        "title": obj.title,
        "description": obj.description,
    }
    assert data == expected_data


@pytest.mark.django_db
def test_review_serializer_update():
    product = ProductFactory()
    variant = ProductVariantFactory(product=product)
    order = OrderFactory()
    OrderItemFactory.create(product_variant=variant, order=order)
    review = ProductReviewFactory(order=order, product=product)
    new_data = {
        "id": review.id,
        "rating": 1,
        "title": "New title",
        "description": "New description",
    }

    serializer = ProductReviewSerializer(review, data=new_data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    expected_data = {
        "id": obj.id,
        "rating": obj.rating,
        "order": obj.order.id,
        "product": obj.product.id,
        "title": obj.title,
        "description": obj.description,
    }
    assert new_data == expected_data


# ------ Comment Serializer -------


@pytest.mark.django_db
def test_comment_serializer_representation():
    comment = ProductCommentFactory()
    serializer = ProductCommentSerializer(comment)

    assert serializer.data == {
        "id": comment.id,
        "product": comment.product.id,
        "commented_by": {
            "id": comment.commented_by.id,
            "full_name": comment.commented_by.full_name,
            "profile_picture": None,
        },
        "title": comment.title,
        "description": comment.description,
        "created_at": serializer.data["created_at"],
        "updated_at": serializer.data["updated_at"],
    }


@pytest.mark.django_db
def test_comment_serializer_creation():
    customer = CustomerFactory()
    product = ProductFactory()

    data = {
        "product": product.id,
        "commented_by": customer.id,
        "title": "Sample title",
        "description": "Sample description",
    }

    serializer = ProductCommentSerializer(data=data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    assert data == {
        "product": obj.product.id,
        "commented_by": obj.commented_by.id,
        "title": obj.title,
        "description": obj.description,
    }


@pytest.mark.django_db
def test_comment_serializer_update():
    product = ProductFactory()
    comment = ProductCommentFactory(product=product)
    new_data = {
        "id": comment.id,
        "title": "New title",
        "description": "New description",
    }

    serializer = ProductCommentSerializer(comment, data=new_data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    expected_data = {
        "id": obj.id,
        "product": product.id,
        "title": obj.title,
        "description": obj.description,
    }
    assert new_data == expected_data
