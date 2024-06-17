from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from product.models import Product, ProductVariant
from ecom_user.models import EcomUser
from tqdm import tqdm

import random
import time


class Command(BaseCommand):
    help = "Generate test data for performance testing product's python aggregate method and in database aggregation method"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--num_products", type=int, default=5, help="Number of products to create"
        )
        parser.add_argument(
            "--variants_per_product",
            type=int,
            default=5,
            help="Number of product variants per product to create",
        )

    def handle(self, *args, **kwargs):
        start_time = time.time()
        num_products = kwargs["num_products"]
        variants_per_product = kwargs["variants_per_product"]
        user, _ = EcomUser.objects.get_or_create(phone="09377964142")
        with transaction.atomic():
            for i in tqdm(range(num_products), desc="Creating random products"):
                product = Product.objects.create(
                    name=f"Product {i}",
                    main_price=random.randint(100, 1000),
                    user=user,
                )
                for j in range(variants_per_product):
                    ProductVariant.objects.create(
                        product=product,
                        variation=f"Variant {j}",
                        stock=random.randint(0, 100),
                        price=random.randint(100, 1000),
                    )
        self.stdout.write(
            self.style.SUCCESS(
                f"""A total of {num_products*variants_per_product} datarows has 
                been created in the database in {time.time()-start_time} seconds.
                """
            )
        )
