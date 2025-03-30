import factory
from ecom_user_profile.tests.profile_factory import CustomerFactory, SellerFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from order.tests.order_factory import OrderFactory
from product.tests.product_factory import ProductFactory

from feedback.models import ProductComment, ProductReview, SellerReview


class ProductReviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductReview

    reviewed_by = factory.SubFactory(CustomerFactory)
    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    rating = FuzzyInteger(1, 5)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")


class ProductCommentFactory(DjangoModelFactory):
    class Meta:
        model = ProductComment

    commented_by = factory.SubFactory(CustomerFactory)
    product = factory.SubFactory(ProductFactory)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")


class SellerReviewFactory(DjangoModelFactory):
    class Meta:
        model = SellerReview

    seller = factory.SubFactory(SellerFactory)
    order = factory.SubFactory(OrderFactory)
    reviewed_by = factory.SubFactory(CustomerFactory)
    rating = FuzzyInteger(1, 5)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
