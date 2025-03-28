import pytest
from django import db
from django.urls import reverse
from ecom_user_profile.tests.profile_factory import CustomerFactory, SellerFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from product.tests.product_factory import (
    ProductFactory,
    ProductVariantFactory,
)
from rest_framework.test import APIClient

from feedback.models import ProductComment, ProductReview
from feedback.serializers import ProductCommentSerializer, ProductReviewSerializer
from feedback.tests.feedback_factory import ProductCommentFactory, ProductReviewFactory


@pytest.fixture
def customer_instance():
    return CustomerFactory()


@pytest.fixture
def seller_instance():
    return SellerFactory()


@pytest.fixture
def api_client_with_customer_credentials(db, customer_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=customer_instance)
    return api_client


@pytest.fixture
def api_client_with_seller_credentials(db, seller_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=seller_instance)
    return api_client


# ---------------
# Product Review
# ---------------


@pytest.mark.django_db
def test_product_review_list(api_client_with_seller_credentials):
    product = ProductFactory()
    reviews = ProductReviewFactory.create_batch(10, product=product)

    url = reverse("product-review-list", kwargs={"pk": product.id})
    response = api_client_with_seller_credentials.get(url)
    assert response.status_code == 200
    assert response.data["count"] == 10

    serializer = ProductReviewSerializer(reviews, many=True)
    assert response.data["results"] == serializer.data


@pytest.mark.django_db
def test_product_review_create(api_client_with_customer_credentials):
    product = ProductFactory()
    product_variant = ProductVariantFactory(product=product)
    order = OrderFactory()
    OrderItemFactory(product_variant=product_variant, order=order)

    url = reverse("product-review-create")
    data = {
        "product": product.id,
        "order": order.id,
        "rating": 5,
        "title": "good product",
        "description": "very goog product",
    }
    response = api_client_with_customer_credentials.post(url, data=data, format="json")

    review = ProductReview.objects.get(id=response.data["id"])
    serializer = ProductReviewSerializer(review)
    assert response.status_code == 201, f"Unexpected response: {response.data}"
    assert response.data == serializer.data


@pytest.mark.django_db
def test_product_review_create_anonymous_not_allowed():
    api_client = APIClient()
    url = reverse("product-review-create")
    response = api_client.post(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_product_review_delete(api_client_with_customer_credentials, customer_instance):
    review = ProductReviewFactory(reviewed_by=customer_instance)

    url = reverse("review-detail", kwargs={"pk": review.id})
    response = api_client_with_customer_credentials.delete(url)

    assert response.status_code == 204, f"Unexpected response: {response.data}"


@pytest.mark.django_db
def test_product_review_update(api_client_with_customer_credentials, customer_instance):
    product = ProductFactory(owner=customer_instance)
    product_variant = ProductVariantFactory(product=product)
    order = OrderFactory()
    OrderItemFactory(product_variant=product_variant, order=order)
    review = ProductReviewFactory(
        reviewed_by=customer_instance, product=product, order=order
    )

    url = reverse("review-detail", kwargs={"pk": review.id})
    new_data = {"title": "New title", "description": "New description"}
    response = api_client_with_customer_credentials.patch(
        url, data=new_data, format="json"
    )

    assert response.status_code == 200, f"Unexpected response: {response.data}"
    assert response.data["title"] == new_data["title"]
    assert response.data["description"] == new_data["description"]


@pytest.mark.django_db
def test_customer_reviews_list(api_client_with_customer_credentials, customer_instance):
    reviews = ProductReviewFactory.create_batch(10, reviewed_by=customer_instance)

    url = reverse("user-reviews")
    response = api_client_with_customer_credentials.get(url)

    serializer = ProductReviewSerializer(reviews, many=True)
    assert response.status_code == 200, f"Unexpected response: {response.data}"
    assert len(response.data.get("results")) == 10
    assert serializer.data == response.data.get("results")


# ---------------
# Product Comments
# ---------------


@pytest.mark.django_db
def test_product_comments_list(api_client_with_seller_credentials):
    product = ProductFactory()
    comments = ProductCommentFactory.create_batch(10, product=product)

    url = reverse("product-comment-list", kwargs={"pk": product.id})
    response = api_client_with_seller_credentials.get(url)
    assert response.status_code == 200
    assert response.data["count"] == 10

    serializer = ProductCommentSerializer(comments, many=True)
    assert response.data["results"] == serializer.data


@pytest.mark.django_db
def test_product_comment_create(api_client_with_customer_credentials):
    product = ProductFactory()

    url = reverse("product-comments-create")
    data = {
        "product": product.id,
        "title": "good product",
        "description": "very goog product",
    }
    response = api_client_with_customer_credentials.post(url, data=data, format="json")
    assert response.status_code == 201, f"Unexpected response: {response.data}"

    comment = ProductComment.objects.get(id=response.data["id"])
    serializer = ProductCommentSerializer(comment)

    assert response.data == serializer.data


@pytest.mark.django_db
def test_product_comment_create_anonymous_not_allowed():
    api_client = APIClient()
    url = reverse("product-comments-create")
    response = api_client.post(url)

    assert response.status_code == 401, f"Unexpected repsonse {response.data}"


@pytest.mark.django_db
def test_product_comment_delete(
    api_client_with_customer_credentials, customer_instance
):
    review = ProductCommentFactory(commented_by=customer_instance)

    url = reverse("comment-detail", kwargs={"pk": review.id})
    response = api_client_with_customer_credentials.delete(url)

    assert response.status_code == 204, f"Unexpected response: {response.data}"


@pytest.mark.django_db
def test_product_comment_update(
    api_client_with_customer_credentials, customer_instance
):
    product = ProductFactory(owner=customer_instance)
    comment = ProductCommentFactory(commented_by=customer_instance, product=product)

    url = reverse("comment-detail", kwargs={"pk": comment.id})
    new_data = {"title": "New title", "description": "New description"}
    response = api_client_with_customer_credentials.patch(
        url, data=new_data, format="json"
    )

    assert response.status_code == 200, f"Unexpected response: {response.data}"
    assert response.data["title"] == new_data["title"]
    assert response.data["description"] == new_data["description"]


@pytest.mark.django_db
def test_customer_product_comments_list(
    api_client_with_customer_credentials, customer_instance
):
    comments = ProductCommentFactory.create_batch(10, commented_by=customer_instance)

    url = reverse("user-comments")
    response = api_client_with_customer_credentials.get(url)

    serializer = ProductCommentSerializer(comments, many=True)
    assert response.status_code == 200, f"Unexpected response: {response.data}"
    assert len(response.data.get("results")) == 10
    assert serializer.data == response.data.get("results")
