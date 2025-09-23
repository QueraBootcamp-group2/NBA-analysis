from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship, Session

username = "root"
password = ""
host = ""   
port = 3306             
database = "NBA"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
metadata = MetaData()
Base = declarative_base()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100)),
)

orders = Table(
    "orders", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product", String(100))
)

metadata.create_all(engine)


class User(Base): 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    orders = relationship("Order", back_populates="user")

class Order(Base): 
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

Base.metadata.create_all(engine)

with Session(engine) as session:
    # Insert users
    for _, row in df_users.iterrows():
        user = User(name=row["name"])
        session.add(user)

    # Insert orders
    for _, row in df_orders.iterrows():
        order = Order(user_id=row["user_id"], product=row["product"])
        session.add(order)

    session.commit()