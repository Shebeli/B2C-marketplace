import pytest
from ecom_user_profile.tests.profile_factory import CustomerFactory, SellerFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from product.serializers import ProductSellerSerializer
from product.tests.product_factory import ProductFactory, ProductVariantFactory

from feedback.serializers import (
    ProductCommentSerializer,
    ProductReviewSerializer,
    SellerReviewSerializer,
)
from feedback.tests.feedback_factory import (
    ProductCommentFactory,
    ProductReviewFactory,
    SellerReviewFactory,
)

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
        "rating": review.rating,
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

    obj = serializer.save(commented_by=customer)
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


# ------ Seller Review Serializer -------


@pytest.mark.django_db
def test_seller_review_serializer_representation():
    seller_review = SellerReviewFactory()
    serializer = SellerReviewSerializer(seller_review)

    expected_data = {
        "id": seller_review.id,
        "reviewed_by": {
            "id": seller_review.reviewed_by.id,
            "full_name": seller_review.reviewed_by.full_name,
            "profile_picture": None,
        },
        "seller": seller_review.seller.id,
        "rating": seller_review.rating,
        "title": seller_review.title,
        "description": seller_review.description,
        "created_at": serializer.data["created_at"],
        "updated_at": serializer.data["updated_at"],
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_seller_review_serializer_creation():
    customer = CustomerFactory()
    seller = SellerFactory()
    order = OrderFactory(customer=customer, seller=seller)

    data = {
        "order": order.id,
        "seller": seller.id,
        "rating": 5,
        "title": "Sample title",
        "description": "Sample description",
    }

    serializer = SellerReviewSerializer(data=data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save(reviewed_by=customer)
    expected_data = {
        "seller": seller.id,
        "order": obj.order.id,
        "rating": obj.rating,
        "title": obj.title,
        "description": obj.description,
    }
    assert data == expected_data


@pytest.mark.django_db
def test_seller_review_serializer_update():
    seller = SellerFactory()
    order = OrderFactory(seller=seller)
    seller_review = SellerReviewFactory(order=order, seller=seller)

    new_data = {
        "id": seller_review.id,
        "rating": 1,
        "title": "New title",
        "description": "New description",
    }

    serializer = SellerReviewSerializer(seller_review, data=new_data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    obj = serializer.save()
    expected_data = {
        "id": obj.id,
        "rating": obj.rating,
        "seller": obj.seller.id,
        "order": obj.order.id,
        "title": obj.title,
        "description": obj.description,
    }
    assert new_data == expected_data
