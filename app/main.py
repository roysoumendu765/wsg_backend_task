from fastapi import FastAPI, BackgroundTasks, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.schemas import TransactionWebhook, TransactionResponse
from app.database import AsyncSessionLocal
from app.crud import create_transaction_if_not_exists, get_transaction_by_id
from app.worker import process_transaction
from app.database import engine, Base
from app import models
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Transaction Webhook Service", lifespan=lifespan)

@app.get("/")
async def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post(
    "/v1/webhooks/transactions",
    status_code=status.HTTP_202_ACCEPTED
)
async def transaction_webhook(
    payload: TransactionWebhook,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    created = await create_transaction_if_not_exists(db, payload)

    if created:
        background_tasks.add_task(
            process_transaction,
            payload.transaction_id
        )
        return {
            "status": "accepted",
            "transaction_id": payload.transaction_id
        }

    transaction = await get_transaction_by_id(db, payload.transaction_id)

    return {
        "status": "already_exists",
        "transaction_id": transaction.transaction_id,
        "current_status": transaction.status
    }


@app.get(
    "/v1/transactions/{transaction_id}",
    response_model=TransactionResponse
)
async def get_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    transaction = await get_transaction_by_id(db, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction