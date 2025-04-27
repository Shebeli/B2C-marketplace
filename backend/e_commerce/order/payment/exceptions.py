from django.utils.translation import gettext_lazy as _
from order.exceptions.errors import ResponseBaseError


class PaymentNotImplementedError(ResponseBaseError):
    http_status = 500
    code = 17
    message = _("The given payment service hasn't been implemented yet.")


class PaymentGatewayNotFoundError(ResponseBaseError):
    http_status = 404
    code = 18
    message = _("The given payment service wasn't found.")


class PaymentRequestError(ResponseBaseError):
    http_status = 502
    code = 19
    message = _("The request to the payment service is malformed.")


class PaymentResponseError(ResponseBaseError):
    http_status = 502
    code = 22
    message = _("Response received from payment gateway service is invalid.  ")


class PaymentTimeoutError(ResponseBaseError):
    http_status = 504
    code = 20
    message = _("Payment service service timed out.")


class PaymentServiceUnavailableError(ResponseBaseError):
    http_status = 503
    code = 21
    message = _("Payment service is unavailable.")


class PaymentGoingOnError(ResponseBaseError):
    http_status = 400
    code = 22
    message = _(
        "A paying payment is already going on, should either cancel the on going payment manually or wait it out until its cancelled by the server."
    )
