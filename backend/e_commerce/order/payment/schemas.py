from typing import Optional

from pydantic import BaseModel


class PaymentRequestResponse:
    result_code: int
    track_id: str
    result_meaning: Optional[str] = None


class PaymentStatusResponse(BaseModel):
    paid_at: str
    status: int
    status_meaning: str
    amount: int
    ref_number: Optional[int] = None
    description: Optional[str] = None
    order_id: Optional[str] = None


