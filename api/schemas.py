from pydantic import BaseModel, Field
from typing import Optional


# ── Orders ──────────────────────────────────────────────
class OrderCreate(BaseModel):
    product: str = Field(..., example="Laptop")
    product_quantity: int = Field(..., gt=0, example=3)


class OrderUpdate(BaseModel):
    product: Optional[str] = Field(None, example="Laptop Pro")
    product_quantity: Optional[int] = Field(None, gt=0, example=5)


class OrderResponse(BaseModel):
    order_id: str
    product: str
    product_quantity: int

    class Config:
        from_attributes = True


# ── Tasks ────────────────────────────────────────────────
class TaskResponse(BaseModel):
    task_id: str
    status: str
    type: str

    class Config:
        from_attributes = True


# Response
class AcceptedResponse(BaseModel):
    task_id: int
    message: str = "Request accepted and being processed"
