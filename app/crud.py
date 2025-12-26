from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models import Transaction

async def create_transaction_if_not_exists(
    db: AsyncSession,
    data
) -> bool:
    transaction = Transaction(
        transaction_id=data.transaction_id,
        source_account=data.source_account,
        destination_account=data.destination_account,
        amount=data.amount,
        currency=data.currency,
        status="PROCESSING"
    )
    db.add(transaction)
    try:
        await db.commit()
        return True
    except IntegrityError as exc:
        await db.rollback()
        if getattr(exc.orig, "sqlstate", None) == "23505":
            return False
        raise

async def get_transaction_by_id(
    db: AsyncSession,
    transaction_id: str
):
    result = await db.execute(
        select(Transaction).where(
            Transaction.transaction_id == transaction_id
        )
    )
    return result.scalar_one_or_none()