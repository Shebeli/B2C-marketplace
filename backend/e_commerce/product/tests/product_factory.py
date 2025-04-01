import factory
from ecom_user_profile.tests.profile_factory import SellerFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    SubCategory,
    Tag,
    TechnicalDetail,
)


class MainCategoryFactory(DjangoModelFactory):
    class Meta:
        model = MainCategory

    name = factory.Sequence(lambda n: f"Maincategory {n}")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    main_category = factory.SubFactory(MainCategoryFactory)


class SubCategoryBreadCrumbFactory(DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Sequence(lambda n: f"SubCategory {n}")
    category = factory.SubFactory(CategoryFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    owner = SubFactory(SellerFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("text")
    subcategory = SubFactory(SubCategoryBreadCrumbFactory)


class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = SubFactory(ProductFactory)
    name = factory.Sequence(lambda n: f"product variant {n}")
    color = factory.Sequence(lambda n: f"#{str(n).zfill(6)}")
    price = FuzzyInteger(100, 5000)
    on_hand_stock = FuzzyInteger(5, 100)


class TechnicalDetailFactory(DjangoModelFactory):
    class Meta:
        model = TechnicalDetail

    product = SubFactory(ProductFactory)
    attribute = factory.Faker("word")
    value = factory.Faker("word")


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"Tag {n}")
