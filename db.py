from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()

aengine = create_async_engine("postgresql+psycopg_async://admin:admin@localhost:5432/test")

