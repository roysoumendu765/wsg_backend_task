from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionWebhook(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: int
    currency: str

class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: int
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime]