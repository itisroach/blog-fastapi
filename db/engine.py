from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

engine = create_async_engine("sqlite+aiosqlite:///./database.db")


Session = async_sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
    expire_on_commit=False,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass



async def get_db():
    db = Session()

    try:
        yield db
    
    finally:
        await db.close()