from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TodosTable(Base):
    __tablename__ = "todos table"

    id_identity = Identity(start=1, increment=1)
    id = Column(Integer, id_identity, primary_key=True)

    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(50), nullable=False)
