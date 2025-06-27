from db import Base
from sqlalchemy.orm import mapped_column, Mapped
from uuid import UUID, uuid4

class UserModel(Base):

    # a name for using on exceptions to let user know which table that they got error
    model_name_for_exceptions = "User"

    __tablename__ = "users"

    password: Mapped[str] = mapped_column()

    username: Mapped[str] = mapped_column(unique=True)

    name: Mapped[str] = mapped_column(default="Unknown")

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)

    