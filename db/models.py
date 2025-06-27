from db import Base
from sqlalchemy.orm import mapped_column, Mapped
from uuid import UUID, uuid5

class User(Base):

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid5)

    password: Mapped[str] = mapped_column()

    username: Mapped[str] = mapped_column(unique=True)