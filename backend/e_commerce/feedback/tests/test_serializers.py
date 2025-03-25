import pytest
from ecom_user_profile.tests.profile_factory import CustomerFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from product.tests.product_factory import ProductFactory, ProductVariantFactory

from feedback.serializers import ProductCommentSerializer, ProductReviewSerializer
from feedback.tests.feedback_factory import ProductCommentFactory, ProductReviewFactory

# ------ Review Serializer -------


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


# ------ Comment Serializer -------


@pytest.mark.django_db
def test_comment_serializer_representation():
    comment = ProductCommentFactory()
    serializer = ProductCommentSerializer(comment)
    assert serializer.data == {
        "id": comment.id,
        "product": comment.product.id,
        "commented_by": comment.commented_by.id,
        "title": comment.title,
        "description": comment.description,
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
        "product": comment.product.id,
        "commented_by": comment.commented_by.id,
        "title": "New title",
        "description": "New description",
    }

    serializer = ProductCommentSerializer(comment, data=new_data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    assert new_data == {
        "product": obj.product.id,
        "commented_by": obj.commented_by.id,
        "title": obj.title,
        "description": obj.description,
    }
