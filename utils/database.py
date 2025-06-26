# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# engine = create_async_engine(
#     "postgresql+asyncpg://postgres:2006@localhost:5432/youtube_clone", echo=True
# )

# AsyncSessionLocal = sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False
# )

# Base = declarative_base()


# async def database():
#     async with AsyncSessionLocal() as db:
#         try:
#             yield db
#         finally:
#             await db.close()


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker

# Asinxron SQLite engine
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=True)

# Asinxron sessiya yaratuvchi
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# ORM modellari uchun asosiy klass
Base = declarative_base()


# Dependency
async def database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
