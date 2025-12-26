# create_tables.py

import asyncio
from app.database import engine, Base
from app import models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())