import random
import time

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from ecom_user.models import EcomUser
from ecom_user_profile.tests.profile_factory import SellerFactory
from feedback.tests.feedback_factory import ProductCommentFactory, ProductReviewFactory
from order.tests.order_factory import OrderFactory, OrderItemFactory
from tqdm import tqdm

from product.models import (
    Category,
    MainCategory,
    ProductVariant,
    SubCategory,
)
from product.tests.product_factory import (
    ProductFactory,
    TechnicalDetailFactory,
)


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
        parser.add_argument(
            "--reviews_per_product",
            type=int,
            default=5,
            help="Number of ProductReview objects to be created for each product",
        )
        parser.add_argument(
            "--comments_per_product",
            type=int,
            default=5,
            help="Number of ProductReview objects to be created for each product",
        )
        parser.add_argument(
            "--technical_per_product",
            type=int,
            default=10,
            help="Number of technical detail objects to be created for each product ",
        )

    def handle(self, *args, **kwargs):
        start_time = time.time()

        num_products = kwargs["num_products"]
        variants_per_product = kwargs["variants_per_product"]
        reviews_per_product = kwargs["reviews_per_product"]
        comments_per_product = kwargs["comments_per_product"]
        technical_detail_per_product = kwargs["technical_per_product"]
        try:
            fake_seller = EcomUser.objects.get(phone="09000000000")
        except EcomUser.DoesNotExist:
            fake_seller = SellerFactory(phone="09000000000", first_name="SELLER TEST FIRST NAME", last_name="SELLER TEST LAST NAME")
            fake_seller.seller_profile.store_name = "فروشگاه تستی چیتی پیتی"
            fake_seller.seller_profile.save()
        fake_customer = EcomUser.objects.get_or_create(phone="09000000001")[0]

        with transaction.atomic():
            # create categories
            maincategory_obj = MainCategory.objects.get_or_create(
                name="Sample Main Category"
            )[0]
            category_obj = Category.objects.get_or_create(
                name="Sample Category", main_category=maincategory_obj
            )[0]
            subcategory_obj = SubCategory.objects.get_or_create(
                name="Sample SubCategory", category=category_obj
            )[0]

            # create products
            for i in tqdm(
                range(num_products),
                desc=(
                    f"Creating products {num_products}, with {variants_per_product} variant per product "
                ),
            ):
                product = ProductFactory.create(
                    subcategory=subcategory_obj,
                    owner=fake_seller,
                )
                TechnicalDetailFactory.create_batch(
                    technical_detail_per_product, product=product
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
                ProductReviewFactory.create_batch(
                    reviews_per_product,
                    product=product,
                    order=order,
                )
                ProductCommentFactory.create_batch(
                    comments_per_product, product=product
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"A total of {num_products} products with {num_products * variants_per_product} product variants "
                f"with a total of {reviews_per_product * num_products} reviews "
                f"and with a total of {comments_per_product * num_products} comments "
                f"has been created in the database in {(time.time() - start_time)} seconds."
            )
        )
