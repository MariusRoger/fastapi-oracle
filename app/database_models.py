from sqlalchemy import Column, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Todos(Base):
    __tablename__ = "todos"

    id_identity = Identity(start=1, increment=1)
    id = Column(Integer, id_identity, primary_key=True)

    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(50), nullable=False)

    owner_username = Column(
        String(50),
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
    )


class Users(Base):
    __tablename__ = "users"

    id_identity = Identity(start=1, increment=1)
    id = Column(Integer, id_identity, primary_key=True)

    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
