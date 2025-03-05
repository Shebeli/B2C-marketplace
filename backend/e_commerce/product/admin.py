from django.contrib import admin
from nested_admin import nested

from .models import (
    Tag,
    Product,
    ProductVariant,
    ProductVariantImage,
    TechnicalDetail,
    Category,
    SubCategoryBreadCrumb,
    MainCategory,
)


class TechincalDetailInline(admin.TabularInline):
    model = TechnicalDetail
    extra = 1
    fields = ("attribute", "value")


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "name",
        "price",
        "image",
        "on_hand_stock",
        "is_enabled",
    )
    readonly_fields = ("reserved_stock", "number_sold")
    show_change_link = True


class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1
    fields = "image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "subcategory",
        "rating",
        "view_count",
        "is_valid",
        "is_enabled",
        "created_at",
    )
    list_filter = ("is_valid", "is_enabled", "subcategory", "rating")
    search_fields = ("name", "description", "owner__username", "tags__name")
    readonly_fields = ("is_valid", "view_count", "created_at")
    filter_horizontal = ("tags",)
    inlines = [
        ProductVariantInline,
        TechincalDetailInline,
    ]
    fieldsets = (
        (
            "Add a new product!",
            {"fields": ("name", "owner", "main_variant", "description")},
        ),
        ("Categorization", {"fields": ("subcategory", "tags")}),
    )
    (
        ("Statisticss"),
        {"fields": ("rating", "view_count", "is_valid", "is_enabled", "created_at")},
    )


class SubCategoryInline(nested.NestedTabularInline):
    model = SubCategoryBreadCrumb
    extra = 1
    # fields = ("name",)


class CategoryInline(nested.NestedTabularInline):
    model = Category
    extra = 1
    inlines = [SubCategoryInline]


@admin.register(MainCategory)
class MainCategoryAdmin(nested.NestedModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [
        CategoryInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "main_category")
    list_filter = ("main_category",)
    search_fields = ("name", "main_category__name")
    inlines = [SubCategoryInline]


@admin.register(SubCategoryBreadCrumb)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "get_main_category")
    list_filter = ("category", "category__main_category")
    search_fields = ("name", "category__name", "category__main_category__name")

    def get_main_category(self, obj):
        return obj.category.main_category.name

    get_main_category.short_description = "Main category"
    get_main_category.admin_order_field = "category__main_category__name"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
