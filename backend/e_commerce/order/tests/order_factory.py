import factory
from ecom_user_profile.tests.profile_factory import (
    CustomerFactory,
    SellerFactory,
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from product.tests.product_factory import ProductVariantFactory

from order.models import Order, OrderItem


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    status = Order.COMPLETED
    tracking_code = FuzzyInteger(100000000, 999999999)
    customer = factory.SubFactory(CustomerFactory)
    seller = factory.SubFactory(SellerFactory)

    # @factory.post_generation
    # def with_status(self, create, extracted, **kwargs):
    #     if extracted:
    #         self.status = extracted
    #         if create:
    #             self.save()


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    submitted_price = factory.LazyAttribute(lambda obj: obj.product_variant.price)
    quantity = FuzzyInteger(1, 10)
