from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError

from order.permissions import IsCartItemOwner
from order.models import Order, Cart, CartItem
from order.serializers import CartItemSerializer

class CartItem(RetrieveUpdateDestroyAPIView):
    """
    Allows an user to add a new cart item, delete or modify one of their cart
    items (The only modification in this case would be the `quantity` field).
    """

    permission_classes = [IsCartItemOwner]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    

class ProductList(ListCreateAPIView):
    """
    GET method:
    Providing a subcategory via query parameter in the URL is required.
    ordering field options: main_price, rating, created_at, view_count.
    if you want the ordering to be descending, use - in front of the field.
    example: ?ordering=-view_count
    tags provided by the query parameter should be seperated by comma.
    example: ?tags=tag1,tag2
    POST method:
    Only for authenticated users and admins. users also should have their
    seller profile verified, otherwise, they will get a 403 error.
    """

    permission_classes = [IsSellerVerified]
    queryset = Product.objects.filter(is_valid=True).with_in_stock()
    serializer_class = ProductListSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ["main_price", "rating", "created_at", "view_count", "in_stock"]
    ordering = ["-created_at", "in_stock"]

    def _validate_subcategory(self) -> None:
        subcategory_name = self.request.query_params.get("subcategory")
        if not subcategory_name:
            raise ValidationError(
                "query parameter 'subcategory' should be provided", "no_query_param"
            )
        if not SubCategory.objects.filter(name__iexact=subcategory_name).exists():
            raise ValidationError("subcategory does not exist", "subcategory_not_found")

    def get_queryset(self):
        self._validate_subcategory()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
