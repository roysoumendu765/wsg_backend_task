import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Transaction
from app.logger import logger

MAX_RETRIES = 3
RETRY_DELAY = 5

async def process_transaction(transaction_id: str):
    logger.info(
        "event=processing_started transaction_id=%s",
        transaction_id,
    )

    attempt = 1

    while attempt <= MAX_RETRIES:
        try:
            logger.info(
                "event=processing_attempt transaction_id=%s attempt=%s",
                transaction_id,
                attempt,
            )
            await asyncio.sleep(30)
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(Transaction).where(
                        Transaction.transaction_id == transaction_id
                    )
                )
                transaction = result.scalar_one_or_none()
                if not transaction:
                    logger.warning(
                        "event=transaction_not_found transaction_id=%s",
                        transaction_id,
                    )
                    return
                transaction.status = "PROCESSED"
                transaction.processed_at = datetime.now(timezone.utc)
                transaction.error_message = None
                await db.commit()
            logger.info(
                "event=processing_success transaction_id=%s",
                transaction_id,
            )
            return
        except Exception as exc:
            logger.error(
                "event=processing_error transaction_id=%s attempt=%s error=%s",
                transaction_id,
                attempt,
                str(exc),
                exc_info=True,
            )
            if attempt == MAX_RETRIES:
                async with AsyncSessionLocal() as db:
                    result = await db.execute(
                        select(Transaction).where(
                            Transaction.transaction_id == transaction_id
                        )
                    )
                    transaction = result.scalar_one_or_none()
                    if transaction:
                        transaction.status = "FAILED"
                        transaction.processed_at = datetime.now(timezone.utc)
                        transaction.error_message = str(exc)
                        await db.commit()

                logger.error(
                    "event=processing_failed transaction_id=%s attempts=%s",
                    transaction_id,
                    MAX_RETRIES,
                )
            else:
                await asyncio.sleep(RETRY_DELAY)

            attempt += 1