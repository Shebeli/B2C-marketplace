from typing import Optional

from pydantic import BaseModel


class PaymentRequestResponse(BaseModel):
    result_code: int
    result_meaning: str
    track_id: int


class PaymentStatusResponse(BaseModel):
    status: int
    paid_at: str
    status_meaning: str
    amount: int
    ref_number: Optional[str] = None
    description: str
    order_id: str


PAYMENT_STATUS_CODES = {
    -1: "Waiting for payment",
    -2: "Internal Error",
    1: "Paid and verified",
    2: "Paid and unverified",
    3: "Cancelled by user",
    4: "Card number is invalid",
    5: "Not enough currency",
    6: "Entered password is incorrect",
    7: "Number of requests cannot exceed the limit",
    8: "Number of payment transactions cannot exceed the limit",
    9: "Daily's total paid amount cannot exceed the limit",
    10: "Card issuer is invalid",
    11: "Switch error",
    12: "Cart is inaccessible",
}

