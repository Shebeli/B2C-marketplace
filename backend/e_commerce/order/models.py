from typing import Union

from django.db import models
from django.db.models import F, Sum
from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from product.models import ProductVariant


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=False
    )
    submitted_price = models.BigIntegerField()
    quantity = models.PositiveSmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def get_total_price(self) -> Union[int, float]:
        return self.product_variant.price * self.quantity

    @property
    def owner(self) -> EcomUser:
        return self.product_variant.owner

    class Meta:
        unique_together = ("order", "product_variant")


# Since the business model is a B2C multi vendor platform and the
# web service is not responsible for centralizing the different
# ordered products from different vendors, thus customers CANNOT add
# items to their cart/orders from different shops, and necessary
# validations should be in place for this matter.


class Order(models.Model):
    """
    Due to business policies, When an order is created, the order cannot be modified
    by the customer with the exception of the order getting cancelled if its only in
    PENDING state.

    The order can also be cancelled depending on the seller's policies if it is in
    other states such as PROCESSING or SHIPPED.

    It is seller's full responsibilty to fully inform the customer of its order
    policies before the purchase, and its the customer's responsiblity to adhere
    to the seller's declared order policies before accepting the order.

    Key business rules and policies:

    1. UNPAID orders should be set to CANCELLED by the web service
    after X amount of time, to release the reserved_stocks.

    2. Cart validations need to be run before attempting to create
    an order using user's current cart items (refer to Cart model business
    policies and validations).

    3. If an order is already in UNPAID state by the customer, then they
    cannot create another order until they cancel the  current order or pay the order.

    4. The customer should be notified either in the web app or by other means
    (such as SMS or email) of any update or changes happend to their order's status.

    5. Stock levels must be updated according to the order's status:
       - Upon order creation (UNPAID status), on_hand_stock should be decreased and
         reserved_stock should be increased in exchange.
       - Upon shipping (SHIPPED status), reserved_stock should decrease.
       - If an order is CANCELLED by the customer, the changes happened in first step
         to on_hand_stock and reserved_stock should be reverted.
       - For REFUNDED orders, appropriate stock changes should be applied according to the seller's
         policies.

    6. If any of the payment gateways are down, then the payment service should be disabled by
    the web service and the disabled payment gateway should be checked on a regular basis to see
    if its functional or not.
    However, in rare scenarios, if all of the payment gateways are down, all UNPAID orders
    statuses will be changed to ONHOLD status to prevent automatic cancellation.
    When a customer retries the payment and one of the payment webgates are functional again,
    then the order's status will be set to UNPAID with the timer X set on their order.
    Also, if all of the payment webservices are disabled, then the creation of any
    orders are disabled until the one of the payment gateways starts working again.

    7. Payment validation is required to ensure order's required payment amount is
    neither underpaid nor overpaid.

    In case of payment discrepancies (by checking the difference between the order's total
    cost and paid amount), necessary actions should be taken to fix the debit or the credit.

    8. Refund policies are set by seller. The web server provides the frameworks and tools
    for sellers to define their refund policies but does not hold responsibility for the refunds.

    Refund Guidelines:
    - Customers can request refunds for defects, incorrect products, or other issues within
        7 days of delivery. The payment held by the web app will be returned to the customer's
        deposit, depending on the seller's policy and whether the product needs to be returned.
    - If the product is returned without any issues found, the customer is responsible for paying
        the shipment costs (both delivery and return) and any related fees. The server should set a
        minimum payment amount for each order to cover these refund-related costs (the minimum
        can be calculated by estimating the shipment cost based on the distance and other
        related factors, or using an external API service for retrieving the estimation).
    """

    ONHOLD = "OH"  # incase the payment gateways are all down, or the support deems so
    UNPAID = "UP"  # the customer hasn't paid the order amount
    PAYING = "PG"  # customer is attempting to pay (in sync for 20 minutes)
    PAID = "PD"  # the order is paid, but the seller hasn't accepted the order yet
    PROCESSING = "PC"  # the seller has accepted the order and is preparing the product for shipment
    SHIPPED = "SH"  # the seller has shipped the product to be delivered to customer
    DELIVERED = "DL"  # the customer has recieved the product
    COMPLETED = "CP"  # no complaints have been recieved from the customer for 7 days after delivery
    CANCELLED = "CC"  # the order is cancelled by customer, seller or the server
    REFUNDED = "RF"  # the customer has refunded the delivered product
    STATUS_CHOICES = {
        ONHOLD: "Onhold",
        UNPAID: "Unpaid",
        PAID: "Paid",
        PROCESSING: "Processing",
        SHIPPED: "Shipped",
        DELIVERED: "Delivered",
        COMPLETED: "Completed",
        CANCELLED: "Cancelled",
        REFUNDED: "Refunded",
    }
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=UNPAID)

    customer = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="bought_orders",
    )
    seller = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="sold_orders",
    )
    customer_address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_notes = models.CharField(max_length=300, blank=True)

    CUSTOMER = "CT"
    SELLER = "SL"
    SERVER = "ST"
    CANCELLED_BY_CHOICES = {
        CUSTOMER: "Customer",
        SELLER: "Seller",
        SERVER: "Server",
    }
    cancelled_by = models.CharField(
        max_length=2,
        choices=CANCELLED_BY_CHOICES,
        blank=True,
    )
    cancel_reason = models.CharField(
        max_length=300, blank=True
    )  # set by customer, seller or system
    refund_reason = models.CharField(max_length=300, blank=True)  # set by customer
    tracking_code = models.CharField(blank=True, max_length=50)  # set by seller

    def get_total_price(self) -> int:
        results = self.items.aggregate(total=Sum(F("submitted_price") * F("quantity")))
        return results["total"]


class Cart(models.Model):
    user = models.OneToOneField(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self) -> Union[int, float]:
        return self.items.aggregate(
            total_price=Sum(F("product_variant__price") * F("quantity"))
        )["total_price"]

    def get_seller(self) -> Union[EcomUser, None]:
        first_item = self.items.first()
        if not first_item.exists():
            return None
        return first_item.product_variant.owner


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=False
    )
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_valid(self) -> bool:
        if not self.product_variant:
            return False
        return self.quantity >= self.product_variant.available_stock

    def get_total_price(self) -> Union[int, float]:
        return self.product_variant.price * self.quantity

    class Meta:
        unique_together = ("cart", "product_variant")

    @property
    def owner(self) -> EcomUser:
        return self.cart.user

    @property
    def seller(self) -> EcomUser:
        return self.product_variant.owner
