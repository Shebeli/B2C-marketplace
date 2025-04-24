from typing import Optional

from ecom_user.models import EcomUser
from pydantic import BaseModel


class OrderCreationSchema(BaseModel):
    user: EcomUser
    customer_address: int
    notes: Optional[str] = None

