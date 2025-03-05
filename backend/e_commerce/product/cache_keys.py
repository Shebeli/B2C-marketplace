SUBCATEGORIES_CACHE_KEY = "subcategories"
FULLCATEGORIES_CACHE_KEY = "fullcategories"


def breadcrumb_cache_key(subcategory_id: int) -> str:
    return f"breadcrumb:{subcategory_id}"
