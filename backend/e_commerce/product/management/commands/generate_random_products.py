import random
import time

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from ecom_user.models import EcomUser
from feedback.models import ProductReview
from feedback.tests.feedback_factory import ProductReviewFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from tqdm import tqdm

from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    SubCategory,
)
from product.tests.product_factory import ProductFactory


class Command(BaseCommand):
    help = "Generate random data for the product and product variants model, with some reviews for the products "

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--num_products", type=int, default=10, help="Number of products to create"
        )
        parser.add_argument(
            "--variants_per_product",
            type=int,
            default=2,
            help="Number of product variants per product to create",
        )

    def handle(self, *args, **kwargs):
        start_time = time.time()
        num_products = kwargs["num_products"]
        variants_per_product = kwargs["variants_per_product"]
        fake_seller= EcomUser.objects.get_or_create(phone="09377964142")[0]
        fake_customer = EcomUser.objects.get_or_create(phone="09300000000")[0]

        with transaction.atomic():
            # create categories
            maincategory_obj = MainCategory.objects.get_or_create(
                name="Sample Main Category"
            )[0]
            category_obj = Category.objects.get_or_create(
                name="Sample Category", main_category=maincategory_obj.id
            )[0]
            subcategory_obj = SubCategory.objects.get_or_create(
                name="Sample SubCategory", category=category_obj.id
            )[0]

            # create products
            for i in tqdm(range(num_products), desc="Creating random products"):
                product = Product.objects.create(
                    name=f"Product {i}",
                    owner=fake_seller,
                    subcategory=subcategory_obj,
                    description="Lorem pentum of the pottaisum catasium calcium, abatatium shalsium. ",
                )
                for j in range(variants_per_product):
                    ProductVariant.objects.create(
                        product=product,
                        name=f"Variant {j}",
                        on_hand_stock=random.randint(0, 100),
                        price=random.randint(100, 1000),
                    )
                product.main_variant = ProductVariant.objects.filter(
                    product=product
                ).first()
                product.save()
                order = OrderFactory.create(customer=fake_customer, seller=fake_seller)
                OrderItemFactory.create(
                    product_variant=product.main_variant, order=order
                )
                product_reviews = ProductReviewFactory(
                    product=product,
                    order=order,
                    reviewed_by=fake_customer,
                )
                product_reviews.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"A total of {num_products * variants_per_product} datarows has been created in the database in {(time.time() - start_time)} seconds."
            )
        )
