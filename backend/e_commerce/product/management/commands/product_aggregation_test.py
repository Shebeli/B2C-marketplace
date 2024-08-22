import time

from django.core.management.base import BaseCommand
from tqdm import tqdm

from product.models import Product


class Command(BaseCommand):
    help = "Benchmark different methods of the given model methods"

    def handle(self, *args, **kwargs):
        # Test aggregate in database
        start_time = time.time()
        for product in tqdm(
            Product.objects.all(), desc="Calculating aggregate method total time..."
        ):
            stock = product.get_available_stock(use_db=True)
        aggregate_duration = time.time() - start_time
        # Test the python method
        start_time = time.time()
        for product in tqdm(
            Product.objects.all(), desc="Calculating pythonic method total time..."
        ):
            stock = product.get_available_stock(use_db=False)
        python_duration = time.time() - start_time
        print(f"Database aggregate duration: {aggregate_duration} seconds")
        print(f"Python method duration: {python_duration} seconds")
        print(
            f"Aggregate method is faster than pythonic method by {python_duration/aggregate_duration} times"
        )
