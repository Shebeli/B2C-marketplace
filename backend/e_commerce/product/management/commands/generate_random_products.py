import random
import time

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from ecom_user.models import EcomUser
from tqdm import tqdm

from product.models import Category, MainCategory, Product, ProductVariant, SubCategory


class Command(BaseCommand):
    help = "Generate random data for the product and product variants model "

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
        user, _ = EcomUser.objects.get_or_create(phone="09377964142")

        with transaction.atomic():
            # create categories
            maincategory_obj = MainCategory.objects.create(name="Sample Main Category")
            category_obj = Category.objects.create(
                name="Sample Category", main_category=maincategory_obj
            )
            subcategory_obj = SubCategory.objects.create(
                name="Sample SubCategory", category=category_obj
            )

            # create products
            for i in tqdm(range(num_products), desc="Creating random products"):
                product = Product.objects.create(
                    name=f"Product {i}",
                    owner=user,
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
        self.stdout.write(
            self.style.SUCCESS(
                f"A total of {num_products * variants_per_product} datarows has been created in the database in {(time.time() - start_time)} seconds."
            )
        )
