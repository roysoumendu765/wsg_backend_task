from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Uncomment the following lines if you want to load environment variables from a .env file
# from dotenv import load_dotenv
# load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

print("Database URL:", DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,   
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()