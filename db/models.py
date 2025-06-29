from db import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String
from uuid import UUID, uuid4


class UserModel(Base):

    # a name for using on exceptions to let user know which table that they got error
    model_name_for_exceptions = "User"

    __tablename__ = "users"

    password: Mapped[str] = mapped_column()

    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    name: Mapped[str] = mapped_column(default="Unknown")

    id: Mapped[UUID] = mapped_column(primary_key=True,default_factory=uuid4)

    

class TokenModel(Base):
    
    __tablename__ = "refresh_tokens"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)

    username: Mapped[str] = mapped_column(
        String, 
        ForeignKey("users.username", onupdate="CASCADE", ondelete="CASCADE"), 
        unique=True, nullable=False
    )

    refresh_token: Mapped[str] = mapped_column()

    expiration: Mapped[int] = mapped_column()