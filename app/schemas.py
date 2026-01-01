from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal
class TransactionWebhook(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: Decimal = Field(gt=0)
    currency: str

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value: Decimal):
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        return value
class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime]